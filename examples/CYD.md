# Preparare la Cheap Yellow Display

Questi esempi sono destinati alla **ESP32-2432S028R**: ESP32 classico, flash da 4 MB, display ILI9341 e touch resistivo XPT2046. La scheda collegata durante la verifica usa un ESP32-D0WD-V3 revisione v3.1. La revisione del chip non identifica la revisione del PCB: annotare anche la sigla stampata sulla scheda prima della presentazione.

Altre CYD possono avere display ST7789, touch capacitivo o ESP32-S3 e richiedere configurazioni diverse. Non basta il nome commerciale per scegliere i pin.

## Librerie necessarie

| Libreria | Versione | Funzione |
| --- | --- | --- |
| Adafruit ILI9341 | 1.6.1 | Controllo del display tramite SPI |
| Adafruit GFX Library | 1.11.11 | Testo, cerchi e primitive grafiche |
| Adafruit BusIO | 1.16.2 | Accesso ai bus usato dalle librerie Adafruit |
| XPT2046_Touchscreen, Paul Stoffregen | 1.4 | Lettura del touch resistivo sul secondo bus SPI |

`Arduino.h`, `SPI.h` ed `esp_system.h` arrivano con il core **Arduino-ESP32 2.0.14**: non installarli come librerie separate. L’esempio non usa TFT_eSPI, LVGL o librerie Wi-Fi. Non occorre modificare `User_Setup.h` o file delle librerie: tutti i pin sono nel sorgente.

## Installazione con Arduino IDE

1. Aggiungere nelle preferenze l’URL per il Gestore schede:
   `https://espressif.github.io/arduino-esp32/package_esp32_index.json`.
2. Nel Gestore schede installare **esp32 di Espressif Systems 2.0.14**.
3. Nel Gestore librerie installare **Adafruit ILI9341 1.6.1** e accettare le dipendenze proposte. Installare poi **Adafruit GFX Library 1.11.11**, **Adafruit BusIO 1.16.2** e **XPT2046_Touchscreen 1.4** di Paul Stoffregen.
4. Controllare le versioni finali: l’installazione automatica delle dipendenze può inizialmente selezionare GFX e BusIO più recenti. Possono comparire anche altre librerie per gli esempi Adafruit, come STMPE610, TouchScreen, TSC2007 e SH110X: non sono usate dalla Sfera di cristallo.
5. Aprire [SferaDiCristallo.ino](arduino-original/SferaDiCristallo/SferaDiCristallo.ino), selezionare **ESP32 Dev Module**, CPU **240 MHz**, flash **4 MB**, modalità **DIO**, frequenza **40 MHz**, partizioni **Default**, PSRAM **Disabled**, **Erase All Flash Before Sketch Upload → Disabled**, caricamento **115200**, quindi la porta seriale.
6. Premere **Verifica**, poi **Carica**. Aprire il monitor seriale a **115200 baud**.

Le cartelle predefinite di Arduino IDE 1.8.19 su Linux sono: core e toolchain in `~/.arduino15/packages/esp32/`, librerie in `~/Arduino/libraries/`. Riavviare l’IDE se era già aperto durante l’installazione. Non copiare le librerie da `.pio` nello sketchbook.

I [comandi Arduino CLI](arduino-original/README.md#comandi-equivalenti-con-arduino-cli) riproducono l’installazione e sono usati dalla CI. Non è necessario installare PlatformIO per compilare lo sketch Arduino.

## Installazione con PlatformIO

Aprire `examples/platformio-single-board` in VSCodium con l’estensione PlatformIO IDE e scegliere **Project Tasks → cyd → General → Build**. PlatformIO legge [platformio.ini](platformio-single-board/platformio.ini) e scarica piattaforma e librerie automaticamente.

- `espressif32 @ 6.5.0` fornisce Arduino-ESP32 2.0.14 e la toolchain.
- Le tre librerie Adafruit sono dichiarate con le versioni della tabella.
- XPT2046_Touchscreen viene scaricata dal repository ufficiale al commit `d57f64c8b5f2bc5b8d10d121550806eeff7b06d9`, corrispondente al tag `v1.4`. Il registro PlatformIO di Paul Stoffregen non offre quella versione: per il download serve **Git**.

Le librerie del progetto sono in `.pio/libdeps/cyd/`; piattaforme e toolchain sono normalmente in `~/.platformio/`. Sono installazioni separate da quelle di Arduino IDE. Non aggiungere `.pio/` a Git e non modificare manualmente le sue librerie.

L’installazione iniziale richiede Internet. Dopo **Build**, scegliere **Upload**, poi **Monitor**. Chiudere il monitor seriale dell’altro ambiente prima del caricamento. I [comandi PlatformIO](platformio-single-board/README.md#comandi-equivalenti-facoltativi) consentono lo stesso flusso da terminale.

## Pin usati

| Segnale | GPIO |
| --- | --- |
| Display SCLK / MOSI / MISO | 14 / 13 / 12 |
| Display CS / DC | 15 / 2 |
| Display RESET | Reset della scheda, `-1` nel costruttore |
| Retroilluminazione, attiva alta | 21 |
| Touch SCLK / MOSI / MISO / CS | 25 / 32 / 39 / 33 |

Il display usa HSPI, il touch VSPI. L’esempio interroga il touch senza interrupt e usa solo pressione e rilascio: non legge coordinate e non richiede calibrazione. Non servono collegamenti esterni, microSD o rete durante l’esecuzione.

## Problemi incontrati su Linux

- **`ModuleNotFoundError: No module named 'serial'`**: il core 2.0.14 invoca `python3` per esptool. Verificare che il Python selezionato disponga di `pyserial`. Avviare l’IDE con il Python di sistema in precedenza nel `PATH`:

  ```sh
  env PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin arduino
  ```

  Verificare con `/usr/bin/python3 -c 'import serial; print(serial.__version__)'`. Se manca anche nel Python di sistema, su Debian/Ubuntu installare `python3-serial` tramite il gestore pacchetti.
- **Porta assente o occupata**: verificare cavo dati, porta, permessi del gruppo `dialout` e altri monitor seriali aperti. Selezionare la porta rilevata sul proprio sistema.
- **`Address "{upload.erase_cmd}" must be a number`** con IDE 1.8.19: selezionare esplicitamente **Erase All Flash Before Sketch Upload → Disabled**. Se si usa la riga di comando dell’IDE, aggiungere `EraseFlash=none` alle opzioni di `--board`.
- **Schermo nero o bianco**: verificare prima sigla CYD, controller e retroilluminazione. La riuscita del caricamento non verifica il display.
- **Touch inattivo**: controllare che sia resistivo XPT2046 e che usi i pin del secondo bus SPI indicati sopra.

Vedere il [protocollo e lo stato delle prove](README.md#verifica-sulla-scheda). Il funzionamento dell’applicazione senza rete non equivale alla disponibilità offline degli strumenti: la prova completa offline è ancora da effettuare.

## Riferimenti

- [Libreria ufficiale Adafruit ILI9341](https://github.com/adafruit/Adafruit_ILI9341).
- [Libreria ufficiale Adafruit GFX](https://github.com/adafruit/Adafruit-GFX-Library).
- [Libreria ufficiale Adafruit BusIO](https://github.com/adafruit/Adafruit_BusIO).
- [XPT2046_Touchscreen v1.4](https://github.com/PaulStoffregen/XPT2046_Touchscreen/tree/d57f64c8b5f2bc5b8d10d121550806eeff7b06d9).
- [Pin e varianti CYD, documentazione comunitaria](https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display).

Le librerie mantengono le proprie licenze; non sono incluse nel repository. Le fonti generali sono raccolte in [notes/sources.md](../notes/sources.md).
