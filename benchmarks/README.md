# Tempi del ciclo di sviluppo

Misure del progetto **Sfera di cristallo** in due sessioni, Linux e Windows. Si misura il tempo reale dal lancio del comando di compilazione alla sua uscita, inclusi analisi delle dipendenze, preprocessore, compilazione, collegamento e creazione del firmware. Non si misurano il tempo di esecuzione sulla scheda, la scrittura del codice o il caricamento via USB.

## Tabella per le slide

**Tempo di attesa dello sviluppatore, in secondi; mediana di tre prove per macchina.** Fra parentesi l'intervallo minimo–massimo. Tutte le 36 compilazioni sono terminate con esito positivo; nessun download o installazione è presente nei log delle due sessioni valide. Arduino Builder 1.6.1 è il motore incluso in Arduino IDE 1.8.19; PlatformIO Core è alla versione 6.2.0.

| Operazione | Motore | Linux | Windows |
| --- | --- | ---: | ---: |
| Compilazione pulita | Arduino Builder | **28,11 s** (27,25–28,16) | **64,78 s** (49,72–69,27) |
| Compilazione pulita | PlatformIO | **14,64 s** (14,40–15,53) | **28,61 s** (28,23–29,01) |
| Senza modifiche | Arduino Builder | **10,92 s** (10,91–11,08) | **15,87 s** (15,63–16,78) |
| Senza modifiche | PlatformIO | **5,49 s** (5,41–5,53) | **5,88 s** (5,31–6,46) |
| Dopo piccola modifica | Arduino Builder | **11,29 s** (11,27–11,47) | **14,89 s** (14,88–16,27) |
| Dopo piccola modifica | PlatformIO | **8,88 s** (8,82–8,92) | **9,77 s** (9,20–11,00) |

Dopo una piccola modifica, in queste sessioni PlatformIO ha ridotto l'attesa di circa **2,41 secondi su Linux** e **5,12 secondi sul PC Windows**. Macchine, CPU, architetture e filesystem sono diversi: le colonne non isolano l'effetto del sistema operativo e le misure non vanno combinate nella stessa mediana. Gli intervalli, in particolare quello delle compilazioni pulite Arduino su Windows, mostrano i limiti di ripetibilità della sessione. Non dimostrano un vantaggio universale.

I dati grezzi restano separati in [results.csv](results.csv) e [results-windows.csv](results-windows.csv). [results-summary.csv](results-summary.csv) conserva mediane, minimi, massimi e numero di prove calcolati dai due CSV: non contiene nuove misure. Per le slide usare due decimali o arrotondare al decimo: la precisione del timer non è la ripetibilità della misura. I CSV pubblici omettono orari precisi, percorsi dei log e identificativi dei computer.

## Ambiente e versioni Linux

| Voce | Configurazione |
| --- | --- |
| Arduino | Arduino Builder 1.6.1, incluso in Arduino IDE 1.8.19 |
| PlatformIO | Core 6.2.0, piattaforma Espressif32 6.5.0 |
| Framework comune | Arduino-ESP32 2.0.14 |
| Toolchain comune | Xtensa ESP32 GCC 8.4.0, esp-2021r2-patch5 |
| Scheda di destinazione | ESP32 Dev Module, CYD ESP32-2432S028R, flash 4 MB |
| Impostazioni | CPU 240 MHz, flash DIO 40 MHz, partizioni Default, PSRAM disabilitata, ottimizzazione `-Os` |
| Parallelismo | 6 processi per entrambi i motori |
| Librerie | ILI9341 1.6.1, GFX 1.11.11, BusIO 1.16.2, XPT2046_Touchscreen 1.4 |

PlatformIO usa il commit ufficiale del tag `v1.4` per XPT2046_Touchscreen. Vedere la [guida CYD](../examples/CYD.md) per installazione e dipendenze. Le versioni delle macro identificative dell’ambiente e i sistemi di compilazione differiscono: il confronto riguarda i due flussi sullo stesso esempio, non due comandi byte per byte identici.

## Metodo

1. Installare preventivamente toolchain e librerie. Le installazioni e le copie dei file non rientrano nei tempi.
2. Creare copie dei due esempi in `.local/benchmarks/<data>/`. I sorgenti originali e il firmware sulla scheda restano invariati.
3. Per ogni ripetizione usare cartelle di compilazione e cache degli oggetti nuove e vuote. Per PlatformIO copiare solo le librerie già scaricate in `.pio/libdeps`, senza `.pio/build`.
4. Misurare una compilazione **pulita**, con core e librerie da compilare.
5. Rilanciare lo stesso comando **senza modifiche**, conservando tutti gli oggetti.
6. Cambiare solo `ATTESA_RISPOSTA_MS = 800;` in `ATTESA_RISPOSTA_MS = 801;` nella copia dello sketch o di `main.cpp`. Misurare la **ricompilazione dopo piccola modifica**, conservando gli oggetti precedenti.
7. Ripetere tre volte, in sequenza: Arduino→PlatformIO, PlatformIO→Arduino, Arduino→PlatformIO. Nessuna compilazione è eseguita contemporaneamente a un’altra.

Il timer Python `time.perf_counter()` comprende l’intera durata del sottoprocesso. Entrambi i comandi usano output normale salvato su file. Il riepilogo usa la **mediana di tre misure** e riporta anche minimo e massimo.

Per Arduino si invoca direttamente **il motore di Arduino IDE 1.8.19**, senza avviare ogni volta Java e l’interfaccia grafica. PlatformIO usa `pio run -e cyd -j 6`. Questo rende il confronto centrato sull’attesa di compilazione: non è una misura del tempo necessario ad aprire VSCodium o Arduino IDE, né del percorso completo clic→risultato nell’interfaccia.

“Pulita” significa cache degli oggetti di compilazione vuota, **non** cache del filesystem o download vuoti. La cache del sistema operativo non viene cancellata. È una misura su una normale macchina di sviluppo, con altri processi e frequenza CPU variabile; tre prove descrivono questa sessione, non garantiscono un vantaggio universale. Il tempo di una modifica a un header condiviso o a una dipendenza può essere diverso.

## Riproduzione

Da questa macchina, dopo l’installazione descritta nella guida CYD:

```sh
/usr/bin/python3 benchmarks/measure.py \
  --ide "$HOME/strumenti/arduino-1.8.19" \
  --rounds 3 --jobs 6
```

Su altre macchine adattare `--ide`, `--data` e `--sketchbook`. Il Python invocato dal core ESP32 deve avere `pyserial`; qui lo script antepone `/usr/bin` al `PATH`. Serve una sola versione installata per ciascun tool Espressif, così lo script non ne seleziona una ambiguamente.

Lo script si ferma se il CSV scelto esiste già, per non sovrascrivere misure registrate: per una nuova sessione passare un nuovo nome a `--output`. Mantenere `results.csv` come sessione Linux originale. I log completi, le copie di lavoro e `metadata.json` con i comandi e i percorsi locali sono in `.local/benchmarks/`, esclusa da Git. Il CSV conserva esito, numero di processi, hash del sorgente e percorso del log per ogni misura.

## Riferimenti

- [Arduino Builder, motore usato da Arduino IDE 1.x](https://github.com/arduino/arduino-builder).
- [Configurazione del progetto PlatformIO](https://docs.platformio.org/en/stable/projectconf/index.html).
- [Cache di compilazione PlatformIO](https://docs.platformio.org/en/latest/projectconf/sections/platformio/options/directory/build_cache_dir.html).

I dati sono misure locali; i collegamenti documentano gli strumenti, non i risultati.

## Ripetere le misure su Windows

Lo script riconosce `arduino-builder.exe`, usa percorsi Windows e accetta `--pio` e `--output`. I risultati Linux restano in `results.csv`: conservare le misure Windows in un CSV distinto e non combinarle nella stessa mediana. Linux e Windows sono due contesti del confronto: con CPU e dischi diversi, le differenze non possono essere attribuite al solo sistema operativo.

### Preparazione

1. Clonare il repository in un percorso breve, per esempio `C:\src\linux-day-2026-platformio`. Installare Git e Python 3.9 o successivo, con il comando `py` disponibile.
2. Scaricare **Arduino IDE 1.8.19 per Windows**, preferibilmente l’archivio ZIP dalla [pagina ufficiale dei download](https://www.arduino.cc/en/software). Estrarlo, per esempio, in `C:\Arduino\arduino-1.8.19`. Serve il file `arduino-builder.exe`: Arduino IDE 2 usa un altro motore e non riproduce questo confronto.
3. Aprire l’IDE e installare core **esp32 2.0.14** e le quattro librerie alle versioni esatte della [guida CYD](../examples/CYD.md#librerie-necessarie). Controllare le versioni dopo l’installazione delle dipendenze. Usare le opzioni della scheda indicate nella guida e premere **Verifica** una volta, senza includere questa compilazione nelle misure.
4. Annotare il percorso dello sketchbook nelle preferenze dell’IDE. La cartella dati standard è `%LOCALAPPDATA%\Arduino15`; un’installazione portabile o proveniente dallo Store può usare altri percorsi. In quel caso passare esplicitamente `--data`.
5. Per mantenere il confronto con la sessione Linux, preparare PlatformIO Core **6.2.0**. In PowerShell, dalla radice del repository:

```powershell
py -3 -m venv .local\benchmark-venv
& .\.local\benchmark-venv\Scripts\python.exe -m pip install "platformio==6.2.0" pyserial
$benchmarkPython = Join-Path $PWD '.local\benchmark-venv\Scripts\python.exe'
$benchmarkPio = Join-Path $PWD '.local\benchmark-venv\Scripts\pio.exe'
& $benchmarkPio --version
& $benchmarkPio run --project-dir examples/platformio-single-board -e cyd -j 6
```

L’ultima compilazione prepara toolchain e `.pio/libdeps/cyd` prima del timer. Git deve essere nel `PATH` per la libreria touch. Non serve collegare la scheda: il benchmark non esegue upload. Le due installazioni devono usare Arduino-ESP32 2.0.14, la stessa toolchain e le stesse librerie; verificare le versioni nei log. Lo script richiede una sola versione installata per ogni strumento nella cartella dati Arduino scelta e si ferma in caso di ambiguità; non rimuove versioni esistenti.

### Esecuzione

Nella stessa sessione PowerShell, adattare il percorso dell’IDE e dello sketchbook:

```powershell
$arduinoIde = 'C:\Arduino\arduino-1.8.19'
$arduinoData = Join-Path $env:LOCALAPPDATA 'Arduino15'
$arduinoSketchbook = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Arduino'
$benchmarkStamp = Get-Date -Format 'yyyyMMdd-HHmmss'
& $benchmarkPython benchmarks/measure.py `
  --ide $arduinoIde `
  --data $arduinoData `
  --sketchbook $arduinoSketchbook `
  --pio $benchmarkPio `
  --output "benchmarks/results-windows-$benchmarkStamp.csv" `
  --rounds 3 --jobs 6
```

Il numero di processi è uguale per entrambi i motori. Per confrontare la stessa impostazione Linux usare `6`; per altre prove scegliere un valore adatto al PC e registrarlo. Collegare il portatile all’alimentazione, annotare il profilo energetico e mantenere costanti le condizioni per tutta la sessione. Registrare CPU, RAM, versione Windows, tipo di disco, versione Python e stato di sincronizzazione della cartella (per esempio OneDrive). Non confrontare i valori assoluti fra computer come se fossero un confronto fra soli sistemi operativi.

Il CSV conserva le 18 misure e i relativi esiti; log, copie di lavoro e `metadata.json` sono in `.local/benchmarks/<data UTC>/`. Il CSV esistente non viene sovrascritto. Se un comando fallisce, la sessione si interrompe: conservare il log, risolvere la causa e ripartire con un nuovo nome di output. Una sessione con download o installazioni durante il timer non è confrontabile con quella Linux: preparare nuovamente le dipendenze e ripetere.

Per condividere i risultati, conservare il CSV e una descrizione dell’ambiente; copiare anche i log e `metadata.json` prima di cambiare macchina, perché `.local/` non viene inviato a Git. Prima di aggiornare le slide, calcolare mediana e minimo–massimo delle tre prove per ogni coppia strumento/scenario e verificare che tutti gli esiti siano zero.

### Verifica dello script

```powershell
py -3 -m unittest discover -s benchmarks -p 'test_*.py'
```

I test controllano ordine delle prove, modifica del solo sorgente copiato, conservazione dei terminatori CRLF, conservazione dei risultati esistenti, modalità di preparazione senza CSV, metadati macchina e arresto dopo un errore. Usano strumenti simulati; la compilazione reale va verificata separatamente con `-PrepareOnly`.

Riferimenti ufficiali: [cartella Arduino15 su Windows](https://support.arduino.cc/hc/en-us/articles/360018448279-Open-the-Arduino15-folder), [installazione PlatformIO Core](https://docs.platformio.org/en/stable/core/installation/methods/installer-script.html).

## Dati pubblici e limiti

I dettagli dei computer ospiti e i metadati locali non sono pubblicati. I valori numerici registrati sono conservati; ogni sistema identifica una sessione distinta. Questa scelta limita la riproducibilità delle condizioni hardware: non usare i risultati per confrontare i sistemi operativi o prevedere le prestazioni su altri computer. Conservare privatamente i metadati di nuove misure prima di condividere un CSV ripulito.
