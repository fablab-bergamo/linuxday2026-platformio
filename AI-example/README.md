# Oracolo: variante animata per la dimostrazione AI

Risultato già preparato per la parte del talk con **Codex integrato in VSCodium**. Il sorgente è stato copiato dal progetto locale `261024-134758-esp32dev`, mantenendo la versione animata già modificata. La piattaforma è fissata a Espressif32 6.5.0; le dipendenze mantengono i riferimenti espliciti del progetto di partenza.

Prompt scelto per la dimostrazione:

> voglio una sfera animata lucicante invece di due cerchi, compila e upload in autonomia

Per ripetere la modifica dal vivo, aprire in VSCodium una copia di `examples/platformio-single-board/`, con i due cerchi originali. Questa cartella conserva il risultato animato da confrontare o usare come riserva. Gli esempi di migrazione e i sorgenti dei benchmark restano separati.

## Compilazione e caricamento

Hardware di riferimento: CYD ESP32-2432S028R, display ILI9341 e touch XPT2046. Pin e dipendenze corrispondono all’esempio iniziale. Dalla radice del repository:

```sh
pio run --project-dir AI-example -e esp32dev
pio run --project-dir AI-example -e esp32dev --target upload
pio device monitor --project-dir AI-example -e esp32dev
```

Collegare la scheda via USB e chiudere altri monitor seriali prima dell’upload. Se occorre selezionare la porta, aggiungere `--upload-port /dev/ttyUSB0` al comando di caricamento, sostituendo il percorso con quello effettivo.

L’animazione usa un buffer `GFXcanvas16` di 112 × 108 pixel e un intervallo minimo tra fotogrammi di 40 ms. Questo intervallo non garantisce 25 fotogrammi al secondo: il tempo di disegno dipende dall’hardware. La sfera continua ad aggiornarsi nel ciclo principale; durante l’attesa della risposta l’animazione accelera. Non sono aggiunte dipendenze grafiche.

## Verifiche

Compilazione locale riuscita il 24 ottobre 2026 con Espressif32 6.5.0 e Arduino-ESP32 2.0.14: 22.268 byte di RAM e 294.621 byte di flash. Il workflow CI è configurato per compilare anche questa variante. Il trasferimento in questa cartella non include una nuova prova fisica: verificare sulla CYD fluidità, tocco, attesa, pressione prolungata, rilascio e nuova risposta. L’upload autonomo richiesto dal prompt dipende dagli strumenti e dai permessi disponibili nella sessione di Codex.

Codice originale e configurazione: licenza MIT, come specificato in `../LICENSE`.
