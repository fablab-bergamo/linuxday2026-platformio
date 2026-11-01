# Linux Day 2026 · Bergamo

Una presentazione sul passaggio da Arduino IDE a PlatformIO, pensata per chi conosce gli sketch Arduino e vuole imparare a organizzare un progetto che cresce nel tempo.

[Apri la presentazione](https://fablab-bergamo.github.io/linuxday2026-platformio/) · [Slide e note del relatore](slides.md) · [Scaletta didattica](notes/outline.md)

## Obiettivi didattici

Il percorso aiuta a:

- distinguere editor, framework Arduino, piattaforma e compilatore;
- migrare uno sketch mantenendo inizialmente framework e comportamento, affrontando un cambiamento alla volta;
- rendere esplicite configurazione e dipendenze, per condividere e riprodurre il progetto;
- valutare tempi di compilazione, supporto C++ e portabilità tra schede attraverso misure e limiti concreti;
- usare l’AI come aiuto facoltativo, verificando le modifiche con compilazione e prove sul dispositivo.

## Il percorso della presentazione

Il filo conduttore è la **Sfera di cristallo**, un piccolo progetto ESP32 con display e touch su Cheap Yellow Display. Si parte dalla versione Arduino IDE e si passa a PlatformIO con una dimostrazione grafica in VSCodium: struttura del progetto, `Arduino.h`, dipendenze in `platformio.ini`, compilazione, caricamento e monitor seriale.

Seguono gestione delle versioni delle librerie, confronto dei tempi misurati su Linux e Windows, navigazione del codice e configurazione dello standard C++. Gli ambienti per più schede introducono il tema delle differenze hardware e della compatibilità delle librerie. Circa cinque minuti sono dedicati all’AI: aggiungere una sfera animata al progetto migrato e verificarne il risultato.

Le misure descrivono i casi provati, senza promettere accelerazioni universali. Il supporto al C++ dipende dalla toolchain scelta; l’assistenza AI è utilizzabile anche in altri ambienti.

## Materiali e stato

- [Esempi eseguibili](examples/README.md): versioni Arduino IDE e PlatformIO, compilate e provate sulla stessa CYD; [variante animata per la demo AI](examples/AI-example/README.md).
- [Benchmark](benchmarks/README.md): metodo, versioni, risultati e script per ripetere le misure.
- [Fonti e attribuzioni](notes/sources.md): riferimenti tecnici e materiali esterni.
- [Guida CYD](examples/CYD.md): configurazione e istruzioni per la scheda.
- [Istruzioni di lavoro](AGENTS.md): avvio locale, build HTML, esportazione PDF e verifiche.

Le slide sono ancora una bozza. Il progetto eseguibile con più schede, la registrazione di riserva e la prova completa offline restano da preparare; occorre inoltre annotare sigla esatta e revisione del PCB della CYD.

## Licenze

Slide e note originali: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). Configurazione, strumenti ed esempi originali: [MIT](LICENSE). Dipendenze e materiali esterni mantengono le proprie licenze; prima di riutilizzare materiale del Libro dei progetti, verificarne la licenza specifica.
