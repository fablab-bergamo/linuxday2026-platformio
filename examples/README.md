# Sfera di cristallo: da Arduino IDE a PlatformIO

Due progetti autonomi con lo stesso comportamento: tocca il display, attendi circa 800 ms e leggi una risposta casuale. La risposta compare anche sul monitor seriale a 115200 baud. Tenere premuto non deve generare risposte ripetute: rilasciare e toccare nuovamente.

- [Versione Arduino IDE](arduino-original/README.md).
- [Versione PlatformIO](platformio-single-board/README.md).
- [Preparazione della CYD: librerie, installazione, pin e problemi su Linux](CYD.md).

## Scheda prevista

Cheap Yellow Display **ESP32-2432S028R**, ESP32 classico, display **ILI9341 320×240** e touch resistivo **XPT2046**. Non presumere la compatibilità di altre CYD, display ST7789, touch capacitivi o schede ESP32-S3. Modello e revisione della scheda dell’utente devono ancora essere confermati. Nessuna connessione a Internet, microSD o componente esterno è necessario durante l’esecuzione; l’installazione iniziale richiede invece Internet.

| Funzione | GPIO |
| --- | --- |
| Display SCLK / MOSI / MISO | 14 / 13 / 12 |
| Display CS / DC / RESET | 15 / 2 / collegato al reset della scheda (-1) |
| Retroilluminazione, attiva alta | 21 |
| Touch SCLK / MOSI / MISO / CS | 25 / 32 / 39 / 33 |

Il touch è letto senza interrupt e senza coordinate: qualsiasi punto attiva la sfera, quindi non serve calibrazione. I caratteri del display sono ASCII; apostrofi sostituiscono gli accenti per evitare problemi con il carattere integrato.

## Cosa cambia nella migrazione

Lo sketch `.ino` e `src/main.cpp` hanno lo stesso corpo; il file C++ aggiunge `#include <Arduino.h>`, inserito automaticamente da Arduino IDE. Le funzioni sono già definite prima dell’uso, quindi non occorrono prototipi aggiuntivi. La scelta della scheda e delle librerie passa dai menu di Arduino IDE a `platformio.ini`.

La grafica usa Adafruit ILI9341 e GFX: non occorre modificare `User_Setup.h` dentro una libreria globale. Il codice dichiara esplicitamente i due bus SPI. Non aggiungere qui differenze funzionali tra le due versioni: questo esempio serve a isolare il cambio di ambiente.

## Verifica sulla scheda

1. Compilare e caricare la versione Arduino IDE: compare il titolo e l’invito a fare una domanda.
2. Toccare: compare l’attesa, poi una risposta leggibile e lo stesso testo sul monitor seriale.
3. Tenere premuto per almeno tre secondi: deve comparire una sola risposta.
4. Rilasciare e toccare: parte una nuova consultazione; la risposta può ripetersi casualmente.
5. Ripetere con PlatformIO sulla stessa scheda e confrontare il comportamento.
6. Riavviare senza connessione di rete: l’applicazione deve continuare a funzionare.

Schermo bianco o nero: verificare prima modello, controller, pin e retroilluminazione. Display funzionante ma nessun tocco: verificare modello resistivo e pin del touch. Per problemi di caricamento, verificare cavo dati, porta e permessi seriali Linux; chiudere altri monitor seriali.

## Stato delle verifiche

Verificata l’identità dei due sorgenti, salvo l’inclusione esplicita di `Arduino.h` nel file C++. Il 18 ottobre 2026 la versione PlatformIO è stata compilata e caricata sulla scheda di riferimento: ESP32-D0WD-V3, revisione v3.1, flash da 4 MB. Piattaforma Espressif32 6.5.0, Arduino-ESP32 2.0.14, toolchain Xtensa 8.4.0+2021r2-patch5. Occupazione: 22.216 byte RAM e 284.773 byte flash. La seriale a 115200 baud conferma `Sfera pronta: tocca lo schermo per una risposta.`

Nella stessa sessione sono state osservate cinque sequenze `Consultazione in corso...` / `Risposta: ...` sulla seriale. L’utente ha successivamente confermato il corretto funzionamento della versione PlatformIO sul display e al touch, dopo la richiesta di provare anche pressione prolungata, rilascio e nuovo tocco.

Sempre il 18 ottobre 2026, lo sketch `.ino` è stato compilato e caricato tramite **Arduino IDE 1.8.19**, usando lo stesso core 2.0.14 e le stesse versioni delle librerie. Occupazione: 22.480 byte RAM e 284.525 byte flash. Esptool ha verificato gli hash del caricamento; la seriale ha mostrato il messaggio di avvio e due coppie consultazione/risposta. L’utente ha confermato anche per questa versione il corretto funzionamento di display, tocco, pressione prolungata, rilascio e nuovo tocco. Sulla scheda è rimasta caricata la versione Arduino IDE.

Il firmware precedente riportava ILI9341 e XPT2046 con pin coerenti con questo esempio. La revisione esatta del PCB resta da annotare. La CI è configurata per entrambe le versioni, ma non è stata eseguita qui. I [tempi di compilazione](../benchmarks/README.md) sono stati misurati separatamente, su copie degli esempi. La prova completa offline resta da effettuare.

## Origine e licenza

Implementazione originale MIT ispirata all’idea della **Sfera di cristallo**, progetto 11 del Libro dei progetti Arduino segnalato dal FabLab. Non è una trascrizione del codice o delle immagini del libro; non riproduce il circuito originale con LCD e sensore di inclinazione.

- [Presentazione del libro sul sito FabLab](https://www.fablabbergamo.it/2026/02/19/arduino-per-principianti-libro-dei-progetti/).
- [Documentazione comunitaria CYD](https://github.com/witnessmenow/ESP32-Cheap-Yellow-Display).
- [Esempio dei bus SPI separati con librerie Adafruit](https://github.com/marcelrv/Cheap-Yellow-Display-ESP32-2432S028R).

Le librerie mantengono le proprie licenze. Nessun file delle librerie è incluso nel repository.
