# Sfera di cristallo con PlatformIO

1. Installare VSCodium e l’estensione **PlatformIO IDE**.
2. Da **File → Apri cartella**, aprire questa cartella (`examples/platformio-single-board`), che contiene `platformio.ini`.
3. Attendere l’installazione iniziale della piattaforma e delle librerie.
4. Nel pannello PlatformIO, aprire **Project Tasks → cyd → General → Build**.
5. Collegare la scheda e scegliere **Upload**, poi **Monitor**. Chiudere prima il monitor di Arduino IDE.
6. Seguire la [verifica comune](../README.md).

Le versioni delle dipendenze sono dichiarate nel progetto. La piattaforma Espressif32 6.5.0 usa Arduino-ESP32 2.0.14: usare la stessa versione del core e delle librerie nel confronto con Arduino IDE.

La libreria XPT2046_Touchscreen viene scaricata dal repository ufficiale, fissata al commit `d57f64c8b5f2bc5b8d10d121550806eeff7b06d9` del tag `v1.4`: quella versione non è disponibile nel registro PlatformIO di Paul Stoffregen. Per installarla serve anche Git.

Se il rilevamento automatico della porta non funziona, impostare `upload_port` e `monitor_port` in `platformio.ini` con la porta effettiva della propria macchina.

## Comandi equivalenti, facoltativi

Da questa cartella:

```sh
pio run -e cyd
pio run -e cyd -t upload
pio device monitor -b 115200
```

La versione PlatformIO è stata compilata, caricata e provata sulla scheda dell’utente il 18 ottobre 2026, con conferma del funzionamento di display e touch. Vedere lo [stato delle verifiche](../README.md#stato-delle-verifiche) per strumenti, limiti e prove ancora da completare.
