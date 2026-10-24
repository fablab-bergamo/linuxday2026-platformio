#!/usr/bin/env python3
"""Misura i tempi di compilazione su copie locali degli esempi, senza upload."""

import argparse
import csv
from contextlib import nullcontext
from datetime import datetime, timezone
import hashlib
import json
import os
import platform
from pathlib import Path
import shutil
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--ide', type=Path, required=True,
                        help='Cartella di Arduino IDE 1.8.19')
    if platform.system() == 'Windows':
        data_default = Path(os.environ.get('LOCALAPPDATA', Path.home() / 'AppData/Local')) / 'Arduino15'
        sketchbook_default = Path.home() / 'Documents/Arduino'
    elif platform.system() == 'Darwin':
        data_default = Path.home() / 'Library/Arduino15'
        sketchbook_default = Path.home() / 'Documents/Arduino'
    else:
        data_default = Path.home() / '.arduino15'
        sketchbook_default = Path.home() / 'Arduino'
    parser.add_argument('--data', type=Path, default=data_default)
    parser.add_argument('--sketchbook', type=Path, default=sketchbook_default)
    parser.add_argument('--pio', type=Path, help='Percorso di pio o pio.exe, se assente dal PATH')
    parser.add_argument('--output', type=Path,
                        help='CSV di destinazione nuovo; predefinito: benchmarks/results.csv')
    parser.add_argument('--prepare-only', action='store_true',
                        help='Compila una copia per strumento, senza creare risultati statistici')
    parser.add_argument('--machine-info', type=Path,
                        help='JSON con le condizioni della macchina da conservare nei metadati')
    parser.add_argument('--rounds', type=int, default=3)
    parser.add_argument('--jobs', type=int, default=6)
    args = parser.parse_args()
    if args.rounds < 1 or args.jobs < 1:
        parser.error('rounds e jobs devono essere positivi')

    root = Path(__file__).resolve().parents[1]
    output = (args.output or root / 'benchmarks/results.csv').resolve()
    if args.prepare_only and args.output:
        parser.error('--prepare-only non accetta --output')
    if not args.prepare_only and output.exists():
        raise FileExistsError(f'{output} esiste già: scegliere un nuovo --output')
    if not args.prepare_only and not output.parent.is_dir():
        parser.error(f'Cartella di destinazione assente: {output.parent}')
    pio = str(args.pio.resolve()) if args.pio else shutil.which('pio')
    if not pio or not Path(pio).is_file():
        parser.error('PlatformIO non trovato: usare il PATH o --pio')
    # Su Windows resolve() espande le junction e annulla l'accorciamento dei comandi GCC.
    absolute = (lambda path: Path(os.path.abspath(path))) if platform.system() == 'Windows' else Path.resolve
    builder = absolute(args.ide) / ('arduino-builder.exe' if platform.system() == 'Windows' else 'arduino-builder')
    if not builder.is_file():
        parser.error(f'Arduino Builder non trovato: {builder}')
    dependencies = root / 'examples/platformio-single-board/.pio/libdeps'
    if not (dependencies / 'cyd').is_dir():
        parser.error('Preparare le dipendenze con pio run -d examples/platformio-single-board -e cyd')
    args.data = absolute(args.data)
    args.sketchbook = absolute(args.sketchbook)
    args.ide = absolute(args.ide)
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    work = root / '.local' / 'benchmarks' / stamp
    work.mkdir(parents=True)
    env = os.environ.copy()
    # Il core ESP32 2.0.14 richiede pyserial nel Python invocato da esptool.
    if platform.system() == 'Linux':
        env['PATH'] = os.pathsep.join(['/usr/bin', '/bin', env['PATH']])
    env['PLATFORMIO_BUILD_CACHE_DIR'] = str(work / 'pio-cache')
    fqbn = ('esp32:esp32:esp32:UploadSpeed=115200,CPUFreq=240,FlashFreq=40,'
            'FlashMode=dio,FlashSize=4M,PartitionScheme=default,DebugLevel=none,'
            'PSRAM=disabled,LoopCore=1,EventsCore=1,EraseFlash=none')
    base = [str(builder), '-compile', '-jobs', str(args.jobs),
            '-hardware', str(args.ide / 'hardware'),
            '-hardware', str(args.data / 'packages'),
            '-tools', str(args.ide / 'tools-builder'),
            '-tools', str(args.ide / 'hardware/tools/avr'),
            '-tools', str(args.data / 'packages'),
            '-built-in-libraries', str(args.ide / 'libraries'),
            '-libraries', str(args.sketchbook / 'libraries'),
            '-fqbn', fqbn, '-core-api-version', '10819',
            '-warnings', 'default']
    # Le versioni installate vengono registrate, senza modificare l'installazione.
    for tool in sorted((args.data / 'packages/esp32/tools').iterdir()):
        versions = sorted(p for p in tool.iterdir() if p.is_dir())
        if len(versions) != 1:
            raise RuntimeError(f'Specificare una sola versione installata per {tool}')
        base += ['-prefs', f'runtime.tools.{tool.name}.path={versions[0]}']

    metadata = {'utc': stamp, 'jobs': args.jobs, 'fqbn': fqbn,
                'prepare_only': args.prepare_only,
                'arduino_command_base': base, 'platformio': pio,
                'platformio_version': subprocess.check_output(
                    [pio, '--version'], text=True).strip(),
                'builder_version': subprocess.check_output(
                    [str(builder), '-version'], text=True).splitlines()[0],
                'uname': list(platform.uname()),
                'cpu_count': os.cpu_count(), 'python': platform.python_version(),
                'load_start': os.getloadavg() if hasattr(os, 'getloadavg') else None}
    if args.machine_info:
        metadata['machine'] = json.loads(args.machine_info.read_text(encoding='utf-8-sig'))
    (work / 'metadata.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    fields = ['utc', 'round', 'tool', 'scenario', 'seconds', 'exit_code',
              'jobs', 'source_sha256', 'log']
    with (nullcontext(None) if args.prepare_only else
          output.open('x', newline='', encoding='utf-8')) as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator='\n') if handle else None
        if writer:
            writer.writeheader()
            handle.flush()
        for trial in range(1, (1 if args.prepare_only else args.rounds) + 1):
            order = ['arduino', 'platformio'] if trial % 2 else ['platformio', 'arduino']
            for tool in order:
                folder = work / f'round-{trial}' / tool
                folder.mkdir(parents=True)
                if tool == 'arduino':
                    project = folder / 'SferaDiCristallo'
                    shutil.copytree(root / 'examples/arduino-original/SferaDiCristallo', project)
                    source = project / 'SferaDiCristallo.ino'
                    build = folder / 'build'
                    cache = folder / 'core-cache'
                    build.mkdir()
                    cache.mkdir()
                    command = base + ['-build-path', str(build),
                                      '-build-cache', str(cache), str(source)]
                else:
                    project = folder / 'project'
                    shutil.copytree(root / 'examples/platformio-single-board', project,
                                    ignore=shutil.ignore_patterns('.pio'))
                    # Dipendenze già scaricate, nessun oggetto compilato copiato.
                    shutil.copytree(dependencies,
                                    project / '.pio/libdeps')
                    source = project / 'src/main.cpp'
                    env['PLATFORMIO_BUILD_CACHE_DIR'] = str(folder / 'cache')
                    command = [pio, 'run', '--project-dir', str(project),
                               '-e', 'cyd', '-j', str(args.jobs)]
                original = source.read_bytes()
                for scenario in (['prepare'] if args.prepare_only else
                                 ['clean', 'unchanged', 'small_edit']):
                    if scenario == 'small_edit':
                        needle = b'ATTESA_RISPOSTA_MS = 800;'
                        if original.count(needle) != 1:
                            raise RuntimeError('Modifica di benchmark non applicabile')
                        source.write_bytes(original.replace(needle, b'ATTESA_RISPOSTA_MS = 801;'))
                    log = folder / f'{scenario}.log'
                    print(f'Prova {trial}: {tool} / {scenario}', flush=True)
                    with log.open('wb') as stream:
                        start = time.perf_counter()
                        result = subprocess.run(command, env=env, stdout=stream,
                                                stderr=subprocess.STDOUT)
                        elapsed = time.perf_counter() - start
                    row = {'utc': datetime.now(timezone.utc).isoformat(),
                           'round': trial, 'tool': tool, 'scenario': scenario,
                           'seconds': f'{elapsed:.6f}', 'exit_code': result.returncode,
                           'jobs': args.jobs,
                           'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
                           'log': log.relative_to(root).as_posix()}
                    if writer:
                        writer.writerow(row)
                        handle.flush()
                    print(f'  {elapsed:.3f} s, esito {result.returncode}', flush=True)
                    if result.returncode:
                        raise RuntimeError(f'Compilazione fallita: leggere {log}')
    print(f'Preparazione completata, log: {work}' if args.prepare_only else
          f'Risultati: {output}', flush=True)


if __name__ == '__main__':
    main()
