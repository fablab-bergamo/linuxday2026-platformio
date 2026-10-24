# Fonti e attribuzioni

## Strumenti per le slide

- Avvio di Slidev: https://sli.dev/guide/
- Compilazione statica: https://sli.dev/guide/hosting
- Esportazione PDF: https://sli.dev/guide/exporting
- Caratteri locali: https://sli.dev/custom/config-fonts

## PlatformIO

- Conversione da .ino a .cpp: https://docs.platformio.org/en/latest/faq/ino-to-cpp.html
- Configurazione: https://docs.platformio.org/en/stable/projectconf/index.html
- Dipendenze: https://docs.platformio.org/en/stable/librarymanager/dependencies.html
- Cache di compilazione: https://docs.platformio.org/en/latest/projectconf/sections/platformio/options/directory/build_cache_dir.html
- Motore di compilazione di Arduino IDE 1.x: https://github.com/arduino/arduino-builder

Le misure locali del ciclo di compilazione sono raccolte in [benchmarks/README.md](../benchmarks/README.md), con dati grezzi in CSV e procedura riproducibile. I tempi non sono ricavati dalla documentazione degli strumenti.

## Scheda ed esempio proposti

- Documentazione ed esempi CYD, comprese istruzioni Arduino IDE: https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display
- Esempio PlatformIO per ESP32-2432S028R: https://github.com/marcelrv/Cheap-Yellow-Display-ESP32-2432S028R
- Libreria touch ufficiale, tag v1.4 usato dagli esempi: https://github.com/PaulStoffregen/XPT2046_Touchscreen/tree/d57f64c8b5f2bc5b8d10d121550806eeff7b06d9
- Librerie display e bus: https://github.com/adafruit/Adafruit_ILI9341, https://github.com/adafruit/Adafruit-GFX-Library, https://github.com/adafruit/Adafruit_BusIO
- Installazione ufficiale Arduino-ESP32: https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html
- Libro dei progetti segnalato dal FabLab: https://www.fablabbergamo.it/2026/02/19/arduino-per-principianti-libro-dei-progetti/

Il FabLab elenca Sfera di cristallo come progetto 11. Il libro online non è stato recuperato: nessun codice del capitolo è stato verificato o copiato. L’articolo indica CC BY-NC-SA 3.0 per il testo citato: non presumere che materiale derivato possa ricevere la licenza MIT o CC BY-SA 4.0 del repository.

## Talk precedente e riferimenti AI

- Resoconto Arduino Day 2026: https://www.fablabbergamo.it/2026/04/01/arduino-day-2026-fablab-bergamo-vibe-coding-ai/
- Slide collegate dal resoconto, non recuperate: https://www.fablabbergamo.it/wp-content/uploads/2026/04/Arduino-Days-2026-Vibe-coding-Arduino.pdf
- Indice delle pubblicazioni di Andreas Spiess: https://www.patreon.com/AndreasSpiess/sitemap
- Progetto pubblico di verifica su hardware: https://github.com/SensorsIot/Embedded-AI-Harness

Aggiungere attribuzioni e licenze quando si introducono risorse esterne. La presentazione usa caratteri di sistema e immagini locali; le risorse esterne sono attribuite nelle sezioni seguenti.

## Loghi nella copertina

- FabLab Bergamo: logo dal [sito ufficiale](https://www.fablabbergamo.it/), [file originale](https://www.fablabbergamo.it/wp-content/uploads/2016/05/Logo_big_biancosotto-300x113.jpg), copia locale in `public/images/fablab-bergamo.jpg`.
- Linux Day: logo ufficiale vettoriale indicato nella [pagina Organizza del Linux Day 2026](https://www.linuxday.it/2026/howto/), [file originale](https://www.linuxday.it/2026/immagini/linuxday_fullcolor.svg), copia locale in `public/images/linuxday.svg`. È il logo generale proposto per l’edizione 2026; l’anno è indicato separatamente nel testo della copertina.

Loghi riprodotti senza modifiche per identificare le rispettive organizzazioni e l’evento; restano dei rispettivi titolari e non sono inclusi nella licenza dei contenuti originali. Fonti consultate il 24 ottobre 2026.

## Illustrazioni e sfondo

`public/images/sfondo-circuito.svg`, `oracolo.svg`, `cyd-schema.svg` e `migrazione.svg` sono illustrazioni vettoriali originali del progetto, distribuite come i contenuti delle slide con CC BY-SA 4.0. Nessuna immagine del libro è riprodotta. La scheda è uno schema illustrativo, non una fotografia del dispositivo; l’interfaccia disegnata è indicativa. Specifiche hardware basate su `examples/CYD.md` e sulla documentazione comunitaria CYD già citata. Tutte le risorse sono locali.

## Libertà degli strumenti e gestione delle dipendenze

Documentazione primaria consultata il 24 ottobre 2026:

- [Piattaforme di sviluppo PlatformIO](https://docs.platformio.org/en/stable/platforms/index.html): ogni piattaforma include script, configurazioni e toolchain per le architetture supportate; non elimina le toolchain specifiche.
- [Pacchetti della piattaforma](https://docs.platformio.org/en/stable/projectconf/sections/env/options/platform/platform_packages.html): configurazione di toolchain, framework e SDK.
- [Gestione dipendenze](https://docs.platformio.org/en/stable/librarymanager/dependencies.html): isolamento per progetto e ambiente, sorgenti alternative, installazione e aggiornamento.
- [lib_deps](https://docs.platformio.org/en/stable/projectconf/sections/env/options/library/lib_deps.html): dichiarazioni nel file di progetto.
- [Specifiche dei pacchetti](https://docs.platformio.org/en/stable/core/userguide/pkg/cmd_install.html#package-specifications): Git a commit/tag, archivi e directory locali; requisiti dei pacchetti e differenza tra copia e collegamento.
- [Arduino Library Registry: FAQ](https://github.com/arduino/library-registry/blob/main/FAQ.md): installazione nello sketchbook e versioni delle librerie.
- [Installazione librerie Arduino IDE 2](https://docs.arduino.cc/software/ide-v2/tutorials/ide-v2-installing-a-library/): Library Manager, ZIP e installazione manuale.
- [Arduino CLI lib install](https://docs.arduino.cc/arduino-cli/commands-reference/arduino-cli_lib_install): anche Arduino CLI supporta sorgenti Git e ZIP.
- [Arduino CLI: sketch project file](https://docs.arduino.cc/arduino-cli/sketch-project-file/): profili sketch.yaml con versioni e compilazione isolata. Evitare il falso confronto «solo PlatformIO può dichiarare dipendenze».

Il caso touch è tratto dal progetto eseguibile e dalla preparazione già documentata in `examples/CYD.md`; il commit completo è importato nelle slide dal file reale. I benchmark sono misure locali in `benchmarks/results.csv` (Linux, 18 ottobre 2026) e `benchmarks/results-windows.csv` (Windows, 24 ottobre 2026), con riepilogo in `benchmarks/results-summary.csv` e metodo in `benchmarks/README.md`. Riguardano Arduino IDE 1.8.19/Builder, non IDE 2. Le colonne rappresentano macchine diverse; non isolano l'effetto del sistema operativo. Le note della slide riportano intervalli e differenze nei commenti dei sorgenti Windows.

## Presentazione del progetto PlatformIO

Fonti ufficiali consultate il 24 ottobre 2026:

- [What is PlatformIO?](https://docs.platformio.org/en/latest/what-is-platformio.html): missione e filosofia; la slide parafrasa la libertà di scelta e la riduzione del vincolo a un produttore. Descrive anche l’ecosistema per più architetture e framework e l’uso tramite editor o CLI.
- [Cronologia delle prime versioni](https://github.com/platformio/platformio-core/blob/v0.10.2/HISTORY.rst), collegata dalle [release notes ufficiali](https://docs.platformio.org/en/latest/core/history.html): prima alpha 0.1.0 il 13 giugno 2014.
- [PlatformIO 2021 Year in Review](https://piolabs.com/blog/news/platformio-year-in-review-2021.html): resoconto del fondatore Ivan Kravets, che descrive il lavoro sul progetto dal 2014.
- [Licenza del Core](https://github.com/platformio/platformio-core/blob/develop/LICENSE): Apache License, Version 2.0. La slide si riferisce al Core attuale, senza attribuire la stessa licenza a ogni componente dell’ecosistema o alle versioni storiche.

- Alieno di PlatformIO: [immagine ufficiale nel repository della documentazione](https://github.com/platformio/platformio-docs/blob/develop/_static/images/platformio-logo.png), copia locale in `public/images/platformio-logo.png`. Logo riprodotto senza modifiche per identificare il progetto; il marchio resta del rispettivo titolare e non rientra nella licenza dei contenuti originali delle slide.

## Arduino IDE e VSCodium

Fonti ufficiali consultate il 24 ottobre 2026:

- [Documentazione Arduino IDE](https://docs.arduino.cc/software/ide/): flusso integrato per sketch, schede, librerie e caricamento; Arduino IDE 2 dispone anche di autocompletamento e debugging.
- [VSCodium](https://vscodium.com/): distribuzione comunitaria di binari liberi basati sui sorgenti di Code - OSS, licenza MIT e telemetria disabilitata.
- [Documentazione VSCodium](https://github.com/VSCodium/vscodium/blob/master/docs/index.md): uso dell’editor e gestione delle estensioni, comprese differenze di catalogo e compatibilità.
- [Guida ufficiale PlatformIO per l’integrazione nell’editor](https://docs.platformio.org/en/latest/integration/ide/vscode.html): integrazione embedded nell’editor e Core CLI. Non equivale a una verifica della stessa estensione su VSCodium.

La raccomandazione di passare a un editor estensibile quando aumentano file, revisioni e strumenti è una scelta didattica del talk, non una limitazione tecnica di Arduino IDE né un obbligo per tutti i progetti hobbistici. Il walkthrough è presentato con VSCodium; l’integrazione grafica completa resta da verificare.

## Fotografia reale della CYD

- Autore del contributo: Andy, account GitHub [Workshopshed](https://github.com/Workshopshed), identificato dalla [cronologia del file](https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display/commit/21f0cd8a81f790a34a950a9d62168b3cb7bf044a).
- [Fotografia originale](https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display/blob/0564a140c76de76ef34a8b7115044e7c6c852695/Examples/NanoFramework/GraphicsExample.jpg), dal repository comunitario CYD di Brian Lough, copia locale integrale in `public/images/cyd-foto.jpg`.
- [Licenza MIT del repository](https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display/blob/0564a140c76de76ef34a8b7115044e7c6c852695/LICENSE), Copyright (c) 2023 Brian Lough; testo conservato in `public/images/cyd-foto-LICENSE.txt`. Il file è esterno alla cartella OriginalDocumentation, esclusa dalla licenza generale del repository.

Foto riprodotta senza modifiche nella slide hardware; mostra un test grafico e non il firmware dell’Oracolo o la scheda fisica dell’utente. La licenza della fotografia resta MIT. Fonte verificata il 24 ottobre 2026.

## Screenshot Arduino IDE e piattaforme supportate

- [Screenshot annotato Arduino IDE 2](https://github.com/arduino/docs-content/blob/main/content/software/ide-v2/tutorials/01.getting-started-ide-v2/assets/ide-2-overview.png), dalla [guida ufficiale](https://docs.arduino.cc/software/ide-v2/tutorials/getting-started-ide-v2/). Copia locale integrale in `public/images/arduino-ide-2.png`, senza modifiche; mostra IDE 2.0.0-rc9, non la sessione dell’Oracolo.
- [Licenza della documentazione Arduino](https://github.com/arduino/docs-content/blob/main/LICENSE.md): testo CC BY-SA 4.0, conservato in `public/images/arduino-ide-2-LICENSE.md`. Attribuzione ad Arduino sulla slide. Le annotazioni originali inglesi sono conservate nell’immagine.
- [Piattaforme supportate](https://docs.platformio.org/en/stable/platforms/index.html) e [framework](https://docs.platformio.org/en/stable/frameworks/index.html): selezione esemplificativa per la slide. Supporto da verificare per specifica combinazione di scheda, piattaforma, framework e versione; non implica portabilità automatica o prove effettuate sulle schede elencate.

## Migrazione guidata, C++ e ambienti

Fonti primarie consultate il 24 ottobre 2026:

- [Conversione manuale da ino a cpp](https://docs.platformio.org/en/latest/faq/ino-to-cpp.html): Arduino.h e dichiarazioni prima delle chiamate nel passaggio manuale a C++.
- [Ambienti PlatformIO](https://docs.platformio.org/en/latest/projectconf/sections/env/index.html): impostazioni comuni in env, sezioni env:nome e selezione con -e.
- [Opzioni di compilazione](https://docs.platformio.org/en/latest/projectconf/sections/env/options/build/build_flags.html) e [rimozione di opzioni](https://docs.platformio.org/en/latest/projectconf/sections/env/options/build/build_unflags.html): esempio opzionale dello standard C++, da verificare rispetto ai flag reali della piattaforma.
- [Standard del linguaggio supportati da GCC](https://gcc.gnu.org/onlinedocs/gcc/Standards.html#C_002b_002b-Language): la disponibilità delle funzionalità dipende anche dalla versione del compilatore e dalla libreria standard.
- [Guida PlatformIO per l’integrazione nell’editor](https://docs.platformio.org/en/latest/integration/ide/vscode.html): Project Tasks e flusso Build, Upload, Monitor.

I frammenti dell’Oracolo sono importati direttamente da main.cpp. La parte AI usa il prompt scelto dall’utente con Codex integrato in VSCodium per animare la sfera, compilare ed eseguire l’upload. Il risultato già modificato è conservato in `AI-example/`, copiato dal progetto locale `261024-134758-esp32dev`; provenienza e verifiche sono descritte nel relativo README. Non sono riportati log di generazione o risultati hardware inventati.

## Specifiche nella slide CYD

- [Repository del progetto CYD, sezione Features](https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display#features): ESP32 con Wi-Fi e Bluetooth, display da 2,8″ a 320 × 240, touch resistivo, USB e slot SD.
- La configurazione di riferimento ESP32-2432S028R, flash da 4 MB, CPU impostata a 240 MHz e controller ILI9341/XPT2046 è documentata in `examples/CYD.md`. Sigla e revisione del PCB fisico restano da annotare; le specifiche non si estendono a tutte le varianti CYD.

## Piattaforma, Core ed estensione

La slide «Il progetto PlatformIO» distingue la piattaforma di sviluppo embedded, il motore PlatformIO Core utilizzabile da CLI e l’estensione PlatformIO IDE per l’interfaccia nell’editor. VSCodium è l’editor scelto per il talk. Riferimenti: [architettura e funzionalità](https://docs.platformio.org/en/latest/what-is-platformio.html) e [Core incluso nell’estensione](https://docs.platformio.org/en/latest/integration/ide/vscode.html#installation). La documentazione ufficiale dell’estensione non certifica il walkthrough su VSCodium: la verifica locale completa resta da eseguire.
