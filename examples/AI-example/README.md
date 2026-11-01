# Oracolo: variante animata per la dimostrazione AI

Risultato già preparato per la parte del talk con **Codex integrato in VSCodium**. Il sorgente è stato copiato dal progetto locale `261024-134758-esp32dev`, mantenendo la versione animata già modificata. La piattaforma è fissata a Espressif32 6.5.0; le dipendenze mantengono i riferimenti espliciti del progetto di partenza.

Prompt scelto per la dimostrazione:

> voglio una sfera animata lucicante invece di due cerchi, compila e upload in autonomia

Per ripetere la modifica dal vivo, aprire in VSCodium una copia di `examples/platformio-single-board/`, con i due cerchi originali. Questa cartella conserva il risultato animato da confrontare o usare come riserva. Gli esempi di migrazione e i sorgenti dei benchmark restano separati.

## Compilazione e caricamento

Hardware di riferimento: CYD ESP32-2432S028R, display ILI9341 e touch XPT2046. Pin e dipendenze corrispondono all’esempio iniziale. Dalla radice del repository:

```sh
pio run --project-dir examples/AI-example -e esp32dev
pio run --project-dir examples/AI-example -e esp32dev --target upload
pio device monitor --project-dir examples/AI-example -e esp32dev
```

Collegare la scheda via USB e chiudere altri monitor seriali prima dell’upload. Se occorre selezionare la porta, aggiungere `--upload-port /dev/ttyUSB0` al comando di caricamento, sostituendo il percorso con quello effettivo.

L’animazione usa un buffer `GFXcanvas16` di 112 × 108 pixel e un intervallo minimo tra fotogrammi di 40 ms. Questo intervallo non garantisce 25 fotogrammi al secondo: il tempo di disegno dipende dall’hardware. La sfera continua ad aggiornarsi nel ciclo principale; durante l’attesa della risposta l’animazione accelera. Non sono aggiunte dipendenze grafiche.

## Simulazione locale con Wokwi

Aprire questa cartella (`examples/AI-example`) in VS Code con le estensioni PlatformIO IDE e Wokwi. Attivare Wokwi secondo la procedura dell’estensione, compilare con **Project Tasks → esp32dev → General → Build**, poi eseguire **Wokwi: Start Simulator** dalla tavolozza comandi.

`diagram.json` usa la scheda nativa `board-esp32-2432s028r`, con display ILI9341 e touch XPT2046 integrati. `wokwi.toml` carica `.pio/build/esp32dev/firmware.bin` e il relativo ELF: viene eseguito lo stesso sorgente della scheda fisica. Dopo lo spostamento della cartella, ricompilare per rigenerare gli artefatti locali.

Premere sul display virtuale, attendere la risposta, poi rilasciare e premere nuovamente; la risposta compare anche sul monitor seriale. La configurazione locale non costituisce una verifica della simulazione o della disponibilità offline. Wokwi è facoltativo: compilazione, upload e uso della scheda restano indipendenti dal simulatore.

Riferimenti: [PlatformIO con Wokwi](https://docs.wokwi.com/vscode/platformio) e [definizione ufficiale della CYD](https://github.com/wokwi/wokwi-boards/blob/main/boards/esp32-2432s028r/board.json).

## Verifiche

Compilazione locale riuscita il 24 ottobre 2026 con Espressif32 6.5.0 e Arduino-ESP32 2.0.14: 22.268 byte di RAM e 294.621 byte di flash. Il workflow CI è configurato per compilare anche questa variante. Il trasferimento in questa cartella non include una nuova prova fisica: verificare sulla CYD fluidità, tocco, attesa, pressione prolungata, rilascio e nuova risposta. L’upload autonomo richiesto dal prompt dipende dagli strumenti e dai permessi disponibili nella sessione di Codex.

Codice originale e configurazione: licenza MIT, come specificato in `../../LICENSE`.
