"""Verifica il protocollo di misura senza compilazioni o modifiche agli esempi."""

import csv
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('measure', Path(__file__).with_name('measure.py'))
measure = importlib.util.module_from_spec(spec)
spec.loader.exec_module(measure)


class MeasurementTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.ide = self.root / 'Arduino IDE'
        self.ide.mkdir()
        (self.ide / 'arduino-builder.exe').touch()
        self.pio = self.root / 'pio.exe'
        self.pio.touch()
        self.data = self.root / 'Arduino15'
        (self.data / 'packages/esp32/tools/compiler/version').mkdir(parents=True)
        self.sketch = self.root / 'examples/arduino-original/SferaDiCristallo/SferaDiCristallo.ino'
        self.main = self.root / 'examples/platformio-single-board/src/main.cpp'
        for source in [self.sketch, self.main]:
            source.parent.mkdir(parents=True)
            source.write_text('// Attesa dell’oracolo\nconst int ATTESA_RISPOSTA_MS = 800;\n', encoding='utf-8')
        (self.main.parents[1] / '.pio/libdeps/cyd').mkdir(parents=True)
        self.output = self.root / 'windows.csv'
        self.argv = ['measure.py', '--ide', str(self.ide), '--data', str(self.data),
                     '--pio', str(self.pio), '--output', str(self.output), '--rounds', '2']
        self.observed = []

    def invoke(self, runner):
        with patch.object(measure, '__file__', str(self.root / 'benchmarks/measure.py')), \
                patch.object(sys, 'argv', self.argv), \
                patch.object(measure.platform, 'system', return_value='Windows'), \
                patch.object(measure.subprocess, 'check_output', return_value='versione di prova\n'), \
                patch.object(measure.subprocess, 'run', side_effect=runner), \
                patch('sys.stdout', new_callable=io.StringIO):
            measure.main()

    def runner(self, command, **kwargs):
        if Path(command[0]).resolve() == self.pio.resolve():
            source = Path(command[command.index('--project-dir') + 1]) / 'src/main.cpp'
            tool = 'platformio'
        else:
            source = Path(command[-1])
            tool = 'arduino'
        self.observed.append((tool, source.read_text(encoding='utf-8')))
        kwargs['stdout'].write(b'Compilazione simulata\n')
        return subprocess.CompletedProcess(command, 0)

    def test_protocol_and_original_sources(self):
        original = self.sketch.read_bytes()
        self.invoke(self.runner)
        with self.output.open(encoding='utf-8', newline='') as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 12)
        self.assertEqual([t for t, _ in self.observed],
                         ['arduino'] * 3 + ['platformio'] * 6 + ['arduino'] * 3)
        for start in range(0, 12, 3):
            group = rows[start:start + 3]
            self.assertEqual([r['scenario'] for r in group], ['clean', 'unchanged', 'small_edit'])
            self.assertEqual(group[0]['source_sha256'], group[1]['source_sha256'])
            self.assertNotEqual(group[1]['source_sha256'], group[2]['source_sha256'])
        self.assertEqual(self.sketch.read_bytes(), original)
        self.assertEqual(self.main.read_bytes(), original)
        self.assertTrue(all((self.root / r['log']).is_file() for r in rows))
        self.assertEqual(len(list((self.root / '.local/benchmarks').glob('*/metadata.json'))), 1)

    def test_existing_results_are_preserved(self):
        self.output.write_text('misure precedenti\n', encoding='utf-8')
        with self.assertRaises(FileExistsError):
            self.invoke(self.runner)
        self.assertEqual(self.output.read_text(encoding='utf-8'), 'misure precedenti\n')
        self.assertFalse((self.root / '.local').exists())

    def test_prepare_only_preserves_results_and_records_machine(self):
        linux_output = self.root / 'benchmarks/results.csv'
        linux_output.parent.mkdir()
        linux_output.write_text('misure Linux\n', encoding='utf-8')
        machine = self.root / 'machine.json'
        machine.write_text(json.dumps({'cpu': 'CPU Windows'}), encoding='utf-8-sig')
        self.argv = self.argv[:self.argv.index('--output')] + [
            '--prepare-only', '--machine-info', str(machine)]
        self.invoke(self.runner)
        self.assertEqual([t for t, _ in self.observed], ['arduino', 'platformio'])
        self.assertEqual(linux_output.read_text(encoding='utf-8'), 'misure Linux\n')
        self.assertFalse(self.output.exists())
        self.assertEqual(list(self.root.rglob('*.csv')), [linux_output])
        metadata_path, = (self.root / '.local/benchmarks').glob('*/metadata.json')
        metadata = json.loads(metadata_path.read_text(encoding='utf-8'))
        self.assertTrue(metadata['prepare_only'])
        self.assertEqual(metadata['machine']['cpu'], 'CPU Windows')

    def test_small_edit_preserves_crlf(self):
        original = b'// Attesa\r\nconst int ATTESA_RISPOSTA_MS = 800;\r\n'
        for source in [self.sketch, self.main]:
            source.write_bytes(original)
        self.invoke(self.runner)
        copied = list((self.root / '.local/benchmarks').rglob('SferaDiCristallo.ino'))
        copied += list((self.root / '.local/benchmarks').rglob('main.cpp'))
        self.assertEqual(len(copied), 4)
        for source in copied:
            self.assertEqual(source.read_bytes(), original.replace(b'800;', b'801;'))

    def test_build_failure_stops_measurement(self):
        def failure(command, **kwargs):
            return subprocess.CompletedProcess(command, 1)
        with self.assertRaisesRegex(RuntimeError, 'Compilazione fallita'):
            self.invoke(failure)
        with self.output.open(encoding='utf-8', newline='') as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]['exit_code'], '1')
        self.assertEqual(self.sketch.read_bytes(), self.main.read_bytes())


if __name__ == '__main__':
    unittest.main()
