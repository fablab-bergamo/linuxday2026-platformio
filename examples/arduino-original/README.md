# Sfera di cristallo con Arduino IDE

Aprire **SferaDiCristallo/SferaDiCristallo.ino**: nome del file e cartella coincidono come richiesto da Arduino IDE.

1. Nelle preferenze, aggiungere l’indice schede ufficiale Espressif: `https://espressif.github.io/arduino-esp32/package_esp32_index.json`.
2. Nel **Gestore schede**, installare **esp32 di Espressif Systems, versione 2.0.14**, corrispondente al framework della configurazione PlatformIO scelta.
3. Selezionare **ESP32 Dev Module**, CPU **240 MHz**, flash **4 MB**, modalità **DIO**, frequenza flash **40 MHz**, schema partizioni **Default**, PSRAM **Disabled**, **Erase All Flash Before Sketch Upload → Disabled** e velocità di caricamento **115200**. Selezionare la porta USB della scheda.
4. Nel **Gestore librerie**, installare le seguenti versioni, controllando anche le dipendenze proposte:

| Libreria | Versione |
| --- | --- |
| Adafruit ILI9341 | 1.6.1 |
| Adafruit GFX Library | 1.11.11 |
| Adafruit BusIO | 1.16.2 |
| XPT2046_Touchscreen di Paul Stoffregen | 1.4 |

5. Premere **Verifica**, poi **Carica**.
6. Aprire il **Monitor seriale** a **115200 baud** e seguire la [verifica comune](../README.md).

Non modificare i file delle librerie. Pin e inizializzazione sono nello sketch. Per la verifica locale è disponibile Arduino IDE 1.8.19; core e librerie sono installati nelle cartelle condivise con l’IDE.

## Comandi equivalenti con Arduino CLI

La CI usa Arduino CLI 1.2.2. Dalla radice del repository:

```sh
arduino-cli core update-index --additional-urls https://espressif.github.io/arduino-esp32/package_esp32_index.json
arduino-cli core install esp32:esp32@2.0.14 --additional-urls https://espressif.github.io/arduino-esp32/package_esp32_index.json
arduino-cli lib update-index
arduino-cli lib install "Adafruit ILI9341@1.6.1" "Adafruit GFX Library@1.11.11" "Adafruit BusIO@1.16.2" "XPT2046_Touchscreen@1.4"
arduino-cli compile --fqbn esp32:esp32:esp32 examples/arduino-original/SferaDiCristallo
arduino-cli upload --fqbn esp32:esp32:esp32 --port /dev/ttyUSB0 examples/arduino-original/SferaDiCristallo
```

Sostituire `/dev/ttyUSB0` con la porta effettiva. L’installazione delle librerie può aggiornare dipendenze automaticamente: al termine controllare con `arduino-cli lib list` che GFX e BusIO abbiano le versioni della tabella.

Per pin, installazione e problemi locali del Python su Linux vedere la [guida CYD](../CYD.md).

## Verifica effettuata

Il 18 ottobre 2026 lo sketch è stato compilato e caricato tramite Arduino IDE 1.8.19 sulla CYD collegata via USB, usando core e librerie indicati sopra. Verificati l’avvio e le risposte sulla seriale; l’utente ha confermato display, touch e comportamento alla pressione prolungata. Occupazione: 284.525 byte flash e 22.480 byte RAM. I [tempi di compilazione](../../benchmarks/README.md) sono stati misurati separatamente, con Arduino Builder. La prova completa offline resta da effettuare.
