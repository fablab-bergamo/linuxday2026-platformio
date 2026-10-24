# Esegue il protocollo con gli strumenti locali preparati per questo repository.
[CmdletBinding()]
param(
    [switch]$PrepareOnly,
    [ValidateRange(1, 256)][int]$Jobs = 6,
    [ValidateRange(1, 100)][int]$Rounds = 3
)

$ErrorActionPreference = 'Stop'
$benchmarkRoot = Split-Path $PSScriptRoot -Parent
$benchmarkTools = Join-Path $benchmarkRoot '.local\benchmark-tools'
$benchmarkPython = Join-Path $benchmarkRoot '.local\benchmark-venv\Scripts\python.exe'
$benchmarkPio = Join-Path $benchmarkRoot '.local\benchmark-venv\Scripts\pio.exe'
$benchmarkIde = Join-Path $benchmarkTools 'arduino-1.8.19'
$benchmarkData = Join-Path $benchmarkTools 'arduino-data'
$benchmarkSketchbook = Join-Path $benchmarkTools 'sketchbook'
foreach ($required in @($benchmarkPython, $benchmarkPio,
        "$benchmarkIde\arduino-builder.exe", "$benchmarkData\packages\esp32\hardware\esp32\2.0.14",
        "$benchmarkSketchbook\libraries", "$benchmarkTools\platformio-core")) {
    if (-not (Test-Path -LiteralPath $required)) {
        throw "Preparazione incompleta: $required. Vedere benchmarks/README.md."
    }
}

$benchmarkStamp = (Get-Date).ToUniversalTime().ToString('yyyyMMddTHHmmssfffffffZ')
$benchmarkMachineFile = Join-Path $benchmarkTools "machine-$benchmarkStamp.json"
$benchmarkOutput = Join-Path $PSScriptRoot "results-windows-$benchmarkStamp.csv"
$benchmarkVolume = Get-Volume -FilePath "$benchmarkRoot\"
$benchmarkBattery = @(Get-CimInstance Win32_Battery | Select-Object BatteryStatus, EstimatedChargeRemaining)
$benchmarkMachine = [ordered]@{
    utc = $benchmarkStamp
    cpu = @(Get-CimInstance Win32_Processor | Select-Object Name, NumberOfCores, NumberOfLogicalProcessors)
    os = Get-CimInstance Win32_OperatingSystem | Select-Object Caption, Version, BuildNumber, TotalVisibleMemorySize
    volume = $benchmarkVolume | Select-Object DriveLetter, FileSystem, Size, SizeRemaining
    disks = @(Get-PhysicalDisk | Select-Object FriendlyName, MediaType, BusType, Size)
    power_scheme = (powercfg /getactivescheme | Out-String).Trim()
    battery = $benchmarkBattery
    repository = $benchmarkRoot
    platformio_core_directory = Join-Path $benchmarkTools 'platformio-core'
    python_packages = @(& $benchmarkPython -m pip freeze)
    git_commit = (git -C $benchmarkRoot rev-parse HEAD | Out-String).Trim()
    git_status = @(git -C $benchmarkRoot status --short)
    jobs = $Jobs
    rounds = $Rounds
    prepare_only = [bool]$PrepareOnly
}
$benchmarkMachine | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $benchmarkMachineFile -Encoding UTF8

$benchmarkOldCore = $env:PLATFORMIO_CORE_DIR
$benchmarkOldPath = $env:PATH
try {
    # I percorsi degli SDK ESP32 ripetuti nei comandi possono superare il limite Windows.
    $benchmarkShortTools = 'B:'
    $benchmarkMappings = (& subst | Out-String)
    if (Test-Path 'B:\') {
        if (-not $benchmarkMappings.Contains("B:\: => $benchmarkTools")) {
            throw 'B: è già occupata: scegliere una lettera libera nel wrapper.'
        }
    } else {
        & subst B: $benchmarkTools
        if ($LASTEXITCODE -ne 0) { throw 'Creazione del percorso breve B: fallita.' }
    }
    $benchmarkIde = "$benchmarkShortTools\arduino-1.8.19"
    $benchmarkData = "$benchmarkShortTools\arduino-data"
    $benchmarkSketchbook = "$benchmarkShortTools\sketchbook"
    $env:PLATFORMIO_CORE_DIR = "$benchmarkShortTools\platformio-core"
    $env:PATH = "$(Split-Path $benchmarkPython -Parent);$benchmarkOldPath"
    $benchmarkArguments = @(
        (Join-Path $PSScriptRoot 'measure.py'),
        '--ide', $benchmarkIde, '--data', $benchmarkData,
        '--sketchbook', $benchmarkSketchbook, '--pio', $benchmarkPio,
        '--machine-info', $benchmarkMachineFile,
        '--rounds', $Rounds, '--jobs', $Jobs
    )
    if ($PrepareOnly) {
        $benchmarkArguments += '--prepare-only'
    } else {
        $benchmarkArguments += @('--output', $benchmarkOutput)
    }
    & $benchmarkPython @benchmarkArguments
    if ($LASTEXITCODE -ne 0) { throw 'Verifica o misura fallita: leggere il log indicato da measure.py.' }
} finally {
    $env:PLATFORMIO_CORE_DIR = $benchmarkOldCore
    $env:PATH = $benchmarkOldPath
}
