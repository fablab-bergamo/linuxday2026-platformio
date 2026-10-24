---
theme: default
title: Da Arduino IDE a PlatformIO
info: Linux Day 2026 · Bergamo
class: text-center
transition: none
routerMode: hash
colorSchema: light
aspectRatio: 16/9
fonts:
  provider: none
  sans: sans-serif
  mono: monospace
---

# Da Arduino IDE a PlatformIO

Da uno sketch a un progetto riproducibile

Linux Day 2026 · Bergamo

Pascal Brunot

<div class="brand-row">
  <img src="/images/fablab-bergamo.jpg" alt="FabLab Bergamo" class="h-20 w-auto" />
  <img src="/images/linuxday.svg" alt="Logo ufficiale Linux Day" class="h-28 w-auto" />
</div>

<!--
Presentazione in italiano. Durata ipotizzata: 35–40 minuti più domande, da confermare.
Presentare un piccolo progetto ESP32 già funzionante in Arduino IDE.
-->

---

# Il percorso

1. Partire da uno sketch Arduino funzionante
2. Migrare il progetto a PlatformIO con VSCodium
3. Dichiarare dipendenze e configurazione di compilazione
4. Preparare la configurazione per una seconda scheda
5. Usare gli strumenti dell’editor e un aiuto mirato dell’AI

<!--
Usare lo stesso progetto durante tutto il percorso. Gli esempi eseguibili sono disponibili e verificati su hardware.
-->

---

# Il progetto che porteremo: l’Oracolo

<div class="visual-grid">
<div>

Ispirato alla **Sfera di cristallo**, progetto 11 di *Arduino: Il Libro dei Progetti*.

- Fai una domanda e tocca lo schermo
- Attendi la risposta casuale dell’Oracolo
- Stesso comportamento con Arduino IDE e PlatformIO

</div>
<img src="/images/oracolo.svg" alt="Illustrazione di una sfera di cristallo con un punto interrogativo" />
</div>

[Il Libro dei Progetti · riferimento sul sito del FabLab Bergamo](https://www.fablabbergamo.it/2026/02/19/arduino-per-principianti-libro-dei-progetti/)

<!--
L’Oracolo è la dimostrazione che porteremo e il filo conduttore della migrazione.
Nel libro il progetto 11 si intitola Sfera di cristallo; nei sorgenti manteniamo
il nome SferaDiCristallo. La nostra implementazione originale adatta l’idea
alla scheda ESP32 con display e touch, senza riprodurre codice o immagini del libro.
Mostrare prima il comportamento: tocco, attesa di circa 800 ms, risposta.
Una pressione prolungata produce una sola risposta; per riprovare occorre rilasciare.
Fonti e attribuzioni in notes/sources.md; esempi eseguibili in examples/.
-->

---

# La scheda: CYD · Cheap Yellow Display

Specifiche della variante **ESP32-2432S028R** usata come riferimento

<div class="visual-grid">
<div>

- **ESP32 · 240 MHz · flash 4 MB**
- **Wi-Fi e Bluetooth** integrati
- Display **2,8″ · 320 × 240**, controller **ILI9341**
- Touch resistivo **XPT2046**, slot **microSD**
- **USB** per alimentazione, programma e seriale

</div>
<div>
<img src="/images/cyd-foto.jpg" alt="Fotografia reale di una Cheap Yellow Display collegata via USB, con barre colorate sullo schermo" class="cyd-photo" />
<p class="visual-caption">Foto: Andy / Workshopshed · progetto CYD · MIT<br>Schermata di prova, non il firmware dell’Oracolo</p>
</div>
</div>

<!--
CYD significa Cheap Yellow Display. Display e touch sono già collegati:
l’Oracolo non richiede cablaggi esterni. Wi-Fi, Bluetooth e microSD non sono
usati dalla demo. I 240 MHz indicano la configurazione CPU scelta per gli esempi.
Gli esempi sono configurati per ESP32-2432S028R; sigla e revisione del PCB
fisico restano da annotare. I controller ILI9341 e XPT2046 e il comportamento
sono già stati verificati sulla scheda usata per la dimostrazione.
Esistono varianti con altri controller o ESP32-S3: il nome commerciale
non garantisce la compatibilità della configurazione. Non entrare nei pin qui.
Riferimenti: examples/CYD.md e notes/sources.md.
-->

---
class: schermata-ide
---

# Arduino IDE: dal codice alla scheda

<img src="/images/arduino-ide-2.png" alt="Screenshot annotato di Arduino IDE 2: verifica, caricamento, scheda, librerie e monitor seriale" class="ide-screenshot" />

<div class="visual-caption">Arduino IDE 2 · schermata dalla documentazione ufficiale Arduino · CC BY-SA 4.0</div>

<!--
Mostrare i comandi familiari: selezionare scheda e porta, verificare, caricare
e aprire il monitor seriale. Il Gestore librerie prepara il confronto successivo.
È lo screenshot ufficiale annotato di Arduino IDE 2.0.0-rc9, non una cattura
della sessione o dello sketch dell’Oracolo. Le annotazioni inglesi fanno parte
dell’immagine originale, riprodotta senza modifiche. Il benchmark misura invece
il motore di IDE 1.8.19: non confondere le due versioni. Fonte in notes/sources.md.
-->

---
class: confronto-editor
---

# Arduino IDE e VSCodium: quando crescere

**Dai primi sketch a un progetto hobbistico che cresce nel tempo.**

| Arduino IDE | VSCodium |
| --- | --- |
| Percorso guidato per imparare e provare uno sketch | Editor generale per organizzare un progetto |
| Scheda, compilazione e caricamento già integrati | Strumenti embedded aggiunti con estensioni o CLI |
| Interfaccia focalizzata sull’esperimento | File, ricerca, Git e terminale nello stesso spazio |
| Poche scelte per partire rapidamente | Ambiente estensibile, con più configurazione iniziale |

<div class="benchmark-note">
VSCodium è una distribuzione libera di Code - OSS. PlatformIO gestisce build e dipendenze.<br>
Anche Arduino IDE 2 offre autocompletamento e debugging: il passaggio riguarda il flusso di lavoro.
</div>

<!--
Messaggio didattico: Arduino IDE permette di concentrarsi su sensore, circuito
e logica senza dover prima costruire l’ambiente. Per un progetto hobbistico
che dura nel tempo, con più file, revisioni, librerie e documentazione,
un editor estensibile rende comodo gestire tutto nello stesso spazio.
È una scelta motivata dalle esigenze: Arduino IDE resta adatto anche a molti
progetti hobbistici e supporta più file C/C++. Non presentarlo come limitato
a script, né sostenere che tutti debbano abbandonarlo. Uno sketch è codice C++.
Git si può usare con entrambi; VSCodium ne integra l’interfaccia nell’editor.
Distinguere tre livelli: VSCodium è l’editor, PlatformIO gestisce compilazione,
strumenti e dipendenze, Arduino resta il framework del nostro firmware.
VSCodium distribuisce binari liberi MIT basati sui sorgenti Code - OSS,
con telemetria disabilitata. La dimostrazione usa VSCodium come editor.
L’integrazione grafica completa va ancora verificata su VSCodium;
il Core è utilizzabile da terminale indipendentemente dall’editor.
Fonti ufficiali e motivazione del confronto in notes/sources.md.
-->

---

# Il progetto PlatformIO

<img src="/images/platformio-logo.png" alt="L’alieno, logo ufficiale di PlatformIO" class="absolute top-5 right-13 h-22 w-22" />

**Sviluppo embedded con libertà di scelta, oltre i vincoli di un singolo produttore.**

- **Piattaforma:** strumenti di sviluppo embedded per più architetture e framework
- **Storia:** prima versione pubblica il **13 giugno 2014**, avviata da **Ivan Kravets**
- **Core (CLI):** compilazione, pacchetti, debugging e test
- **Estensione PlatformIO IDE:** interfaccia grafica nel nostro editor, **VSCodium**
- **Licenza del Core:** **Apache-2.0**, libera e permissiva

<div class="benchmark-note">
Fonti ufficiali: <a href="https://docs.platformio.org/en/latest/what-is-platformio.html">missione</a> · <a href="https://github.com/platformio/platformio-core/blob/v0.10.2/HISTORY.rst">storia</a> · <a href="https://github.com/platformio/platformio-core/blob/develop/LICENSE">licenza</a>
</div>

<!--
Missione parafrasata dalla pagina ufficiale «What is PlatformIO?»: libertà
per sviluppatori e gruppi di lavoro, flessibilità nella scelta di hardware,
framework ed editor e riduzione della dipendenza da un singolo produttore.
PlatformIO è la piattaforma; PlatformIO Core è il motore utilizzabile anche
da terminale. PlatformIO IDE è l’estensione che porta i comandi nell’editor;
VSCodium è l’editor scelto per il talk. L’integrazione grafica completa su
VSCodium resta da verificare sulla macchina della demo. In questa presentazione usiamo VSCodium e manteniamo Arduino.
La cronologia ufficiale riporta la prima alpha 0.1.0 il 13 giugno 2014.
Il fondatore Ivan Kravets racconta il percorso dal 2014 nel resoconto
ufficiale PlatformIO Labs «2021 Year in Review».
Il progetto è cresciuto dal sistema di compilazione e gestione librerie
all’ecosistema documentato oggi. Non confondere la nascita del Core con
quella dell’estensione per l’editor. Apache-2.0 è la licenza attuale del Core:
non attribuirla retroattivamente a tutte le versioni né estenderla a
librerie, toolchain, SDK o servizi, che conservano le proprie condizioni.
Il flusso mostrato non richiede servizi a pagamento. Fonti in notes/sources.md.
-->

---

# Quali tecnologie supporta?

| Famiglia o piattaforma | Esempi di schede |
| --- | --- |
| **Espressif ESP32 / ESP8266** | CYD, ESP32 DevKit, NodeMCU |
| **ST STM32** | Nucleo, Discovery |
| **Microchip AVR / megaAVR / SAM** | Arduino Uno R3, Mega 2560, Nano Every, Due |
| **Raspberry Pi RP2040** | Pico |
| **Nordic nRF52 · Teensy** | nRF52 DK · Teensy |

**Framework:** Arduino, ESP-IDF, STM32Cube, CMSIS, libopencm3 e altri.

<div class="benchmark-note">Il supporto dipende dalla combinazione scheda, piattaforma e framework.<br>Per l’Oracolo: ESP32 + framework Arduino. Fonti: <a href="https://docs.platformio.org/en/stable/platforms/index.html">piattaforme</a> · <a href="https://docs.platformio.org/en/stable/frameworks/index.html">framework</a>.</div>

<!--
Elenco esemplificativo, non esaustivo, dalla documentazione ufficiale.
Arduino indica sia un ecosistema di schede, basate su famiglie diverse,
sia il framework. Non tutte le combinazioni della tabella e dei framework
sono supportate. Controllare la pagina della scheda, la piattaforma e le
versioni prima di promettere portabilità: pin, periferiche e librerie cambiano.
RP2040 non implica automaticamente ogni successiva famiglia Raspberry Pi.
Teensy è una linea di schede con una piattaforma dedicata, non una singola
architettura. Non presentiamo queste schede come ambienti già compilati.
La demo resta sulla CYD; seconda scheda ancora da scegliere.
-->

---

# Una migrazione, un passo alla volta

<div class="visual-grid">
<div>

- Mantenere inizialmente il framework Arduino
- Spostare lo sketch in un progetto strutturato
- Dichiarare scheda e dipendenze in `platformio.ini`
- Compilare, caricare e verificare il comportamento sulla scheda

</div>
<img src="/images/migrazione.svg" alt="Dallo sketch Arduino al progetto con src/main.cpp e platformio.ini" />
</div>

<!--
Gli esempi originali Arduino IDE e PlatformIO sono presenti nel repository,
compilati e verificati sulla Cheap Yellow Display con conferma dell’utente.
Sigla esatta e revisione del PCB ancora da annotare.
Esempio scelto: Sfera di cristallo ispirata al progetto 11 del Libro dei progetti.
Versioni in examples/arduino-original e examples/platformio-single-board.
-->

---

# Perché passare a PlatformIO?

- **Libertà di scegliere:** un flusso comune per più produttori
- **Dipendenze per progetto:** sorgenti e versioni dichiarati
- **Configurazione condivisa:** scheda, framework e opzioni in Git
- **Più ambienti:** varianti hardware nello stesso progetto
- **Verifiche automatizzabili:** compilazioni e test anche fuori dall’editor

Il cuore della migrazione: rendere esplicito ciò che serve al progetto.

<!--
Dedicare il centro del talk alla gestione delle dipendenze. È un beneficio
concreto anche prima di usare più schede o strumenti avanzati.
L’editor aggiunge navigazione, Git ed estensioni; AI opzionale per cinque minuti.
Le funzioni C++ dipendono dalla toolchain. Fonti in notes/sources.md.
-->

---

# Librerie: dal computer al progetto

| Nel flusso abituale di Arduino IDE | Con `lib_deps` in PlatformIO |
| --- | --- |
| Installo una libreria nello sketchbook | Dichiaro la dipendenza nel progetto |
| La versione installata serve più sketch | Ogni progetto può avere la sua versione |
| Documento a parte cosa installare | Sorgente e versione viaggiano con il codice |
| Su un altro PC ripeto la preparazione | La compilazione installa le dipendenze dichiarate |

**Aggiornare l’Oracolo non deve cambiare le librerie di un altro progetto.**

<!--
Distinguere il catalogo Arduino Libraries Index dal Library Manager e dal
modello di installazione: il vantaggio non è avere un catalogo più grande.
Scenario concreto: A continua a usare GFX 1.11.11; in B proviamo una versione
successiva. Le dipendenze PlatformIO sono isolate per progetto e ambiente.
La dichiarazione delle versioni va in Git; .pio resta una cache rigenerabile.
Confronto con il normale uso grafico di Arduino IDE, non con ogni possibilità
dell’ecosistema Arduino: Arduino CLI offre profili sketch.yaml con versioni
fissate e compilazione isolata. Anche Arduino IDE permette ZIP e librerie manuali.
Non promettere riproducibilità assoluta: contano anche dipendenze transitive,
piattaforma, toolchain, disponibilità delle sorgenti e configurazione.
-->

---

# Il catalogo è un punto di partenza

In `lib_deps` possiamo indicare:

- **Registro:** una libreria e una versione precisa
- **Repository Git:** un tag o un commit dell’autore
- **Un nostro fork:** una correzione ancora non pubblicata
- **Archivio o cartella locale:** una libreria del nostro progetto

**La scelta della sorgente diventa parte della configurazione.**

<!--
«Qualsiasi libreria» significa libertà di scegliere la provenienza, non
compatibilità automatica con qualsiasi codice: API, framework, architettura,
struttura del pacchetto e licenza devono essere adatti. L’accesso Git richiede Git.
Arduino può installare ZIP o librerie manuali e Arduino CLI può installare da Git:
il vantaggio mostrato è dichiarare sorgente e riferimento nel normale flusso
PlatformIO, insieme alle altre dipendenze, con installazione automatizzata.
Caso fork: correggere nella propria copia del repository, fissare un commit e
condividerne l’URL; evitare modifiche a mano nella cache .pio/libdeps.
Un branch cambia nel tempo; un commit completo identifica la revisione scelta.
-->

---
class: dipendenze-code
---

# Nell’Oracolo lo facciamo già

Configurazione importata dal progetto eseguibile:

<<< @/examples/platformio-single-board/platformio.ini

Il display arriva dal registro; il touch dal repository ufficiale, a un **commit preciso**.

<!--
Mostrare lib_deps nel file reale aperto in VSCodium. Le tre librerie Adafruit
hanno una versione esatta; il riferimento XPT2046 identifica il commit del tag v1.4.
Nella preparazione documentata il registro PlatformIO non offriva quella versione:
abbiamo indicato direttamente la sorgente ufficiale, senza attendere il catalogo.
È un caso reale, già compilato e verificato sulla scheda; nessun nuovo firmware
è introdotto da queste slide. L’URL lungo è voluto: mostra il riferimento effettivo.
Passare poi alla vista delle librerie del progetto e alla compilazione.
Non modificare una dipendenza solo per la dimostrazione; spiegare invece come
provare un aggiornamento su un ramo Git, compilare e verificare display e touch.
-->

---

# Quanto aspettiamo per compilare?

**Oracolo · secondi · mediana di tre prove · meno è meglio**

Ogni cella: Arduino IDE 1.8.19¹ / **PlatformIO Core 6.2.0**

| Operazione | Linux | Windows |
| --- | ---: | ---: |
| Compilazione pulita | 28,11 / **14,64** | 64,78 / **28,61** |
| Senza modifiche | 10,92 / **5,49** | 15,87 / **5,88** |
| Dopo piccola modifica | 11,29 / **8,88** | 14,89 / **9,77** |

Dopo una modifica: **−2,41 s su Linux · −5,12 s sul PC Windows**.

<div class="benchmark-note">
Macchine e filesystem diversi: non è un confronto fra soli sistemi operativi.<br>
Stesso Arduino-ESP32 2.0.14, GCC e librerie · 6 processi per entrambi i motori.<br>
¹ Builder senza interfaccia grafica. Download e upload esclusi; IDE 2 non misurato.
</div>

<!--
Sessione Linux: hardware ospite non pubblicato.
Sessione Windows: hardware ospite non pubblicato.
18 compilazioni riuscite per macchina; nessun download o installazione nei log misurati.
Metodo completo in benchmarks/README.md; dati grezzi in benchmarks/results.csv
e benchmarks/results-windows.csv.
Riepilogo calcolato dai CSV in benchmarks/results-summary.csv.
Timer esterno: analisi dipendenze, preprocessore, compilazione, link e firmware.
Stesso progetto CYD, impostazioni comparabili, -Os, toolchain Xtensa GCC 8.4.0 esp-2021r2-patch5.
PlatformIO Espressif32 6.5.0; Arduino Builder 1.6.1 di Arduino IDE 1.8.19.
Pulita: oggetti vuoti, dipendenze già scaricate, cache del filesystem non svuotata.
Piccola modifica: ATTESA_RISPOSTA_MS da 800 a 801 nella copia del sorgente.
Linux, intervalli min–max Arduino / PlatformIO: pulita 27,25–28,16 / 14,40–15,53;
senza modifiche 10,91–11,07 / 5,41–5,53; modifica 11,27–11,48 / 8,81–8,92.
Windows: pulita 49,72–69,27 / 28,23–29,01; senza modifiche 15,63–16,78 / 5,31–6,46;
modifica 14,88–16,27 / 9,20–11,00. Evidenziare la variabilità delle pulite Arduino.
Le sessioni non sono state eseguite in un ambiente dedicato e isolato.
La terza ripetizione PlatformIO Windows include quattro commenti #region/#endregion
aggiunti durante la sessione: copie identiche dopo aver rimosso solo questi commenti,
stessa configurazione e logica. Gli hash effettivi restano nei dati grezzi.
Le due sessioni non vanno aggregate: CPU, architettura e filesystem sono diversi.
Tre prove per macchina descrivono queste sessioni, senza un vantaggio universale.
Non misuriamo download,
apertura editor, upload o velocità del firmware. Non estendere i dati a IDE 2.
-->

---
layout: center
class: text-center
---

# Ora migriamo l’Oracolo

**Lo stesso firmware, un progetto esplicito.**

Apri cartella → Sorgenti → Dipendenze → Build → Upload → Monitor

<!--
Inizio della dimostrazione guidata: circa 6 minuti, oltre alla spiegazione delle
dipendenze già fatta. Mostrare il dispositivo funzionante prima di aprire l’editor.
Usare examples/platformio-single-board come cartella radice, non tutto il repository.
Per mostrare la migrazione da zero, lavorare in una copia locale e conservare
l’esempio versionato come riferimento. Non modificare pin o librerie in diretta.
-->

---

# 1 · Aprire il progetto giusto

**VSCodium → File → Apri cartella → `platformio-single-board`**

```text
platformio-single-board/
├── platformio.ini       scheda, framework, dipendenze
└── src/
    └── main.cpp         il nostro sketch, in C++
```

- `include/`: eventuali intestazioni condivise
- `lib/`: eventuali librerie private del progetto
- `.pio/`: pacchetti locali e risultati della build; fuori da Git

<!--
Le prime due sono le sole cartelle/file necessari nell’esempio attuale; include
 e lib sono convenzioni disponibili, non directory da creare vuote.
Se si parte da PlatformIO Home, New Project: scegliere il nome, ESP32 Dev Module
e Arduino. Per questa CYD la configurazione hardware è nei sorgenti, non nel nome
esp32dev. Poi copiare la configurazione già verificata del repository.
La prima installazione può richiedere rete e tempo: prepararla prima del talk.
-->

---

# 2 · Da `.ino` a `src/main.cpp`

**Copiare lo sketch, poi rendere esplicito ciò che Arduino prepara.**

<<< @/examples/platformio-single-board/src/main.cpp#inclusioni

- Aggiungere `#include <Arduino.h>`
- Dichiarare le funzioni prima di chiamarle
- Conservare `setup()` e `loop()`: il framework resta Arduino

<!--
Aprire affiancati examples/arduino-original/SferaDiCristallo/SferaDiCristallo.ino
 e il main.cpp. Nel nostro sorgente le funzioni sono già definite prima dell’uso:
non serve aggiungere prototipi superflui. In altri sketch il preprocessore Arduino
li inserisce, mentre in cpp vanno scritti o le definizioni vanno riordinate.
Non aggiungere una propria main(): l’avvio è fornito dal framework Arduino.
Riferimento: documentazione PlatformIO sulla conversione ino-to-cpp.
-->

---

# La logica resta riconoscibile

Un tocco avvia l’attesa; il ciclo continua a leggere il touch.

<<< @/examples/platformio-single-board/src/main.cpp#risposta

**Cambiamo ambiente di sviluppo; manteniamo il comportamento.**

<!--
Il frammento è importato dal codice eseguibile, non riscritto per le slide.
Richiamare il filtro di 50 ms e il rilevamento della transizione, definiti poco
sopra nel file: una pressione prolungata non genera risposte ripetute.
La sottrazione unsigned tra millis è intenzionale. Evitare una digressione
sull’intera macchina a stati: il tema qui è migrare e verificare lo stesso progetto.
-->

---

# 3 · Compilare, caricare, osservare

**PlatformIO → Project Tasks → cyd → General**

| Comando | Cosa verificare |
| --- | --- |
| **Build** | Dipendenze risolte e compilazione riuscita |
| **Upload** | Scheda e porta corrette, trasferimento completato |
| **Monitor** | Messaggi seriali a **115200 baud** |

Sulla CYD: **tocca → attendi → leggi → rilascia → riprova**.

<!--
Collegare la CYD già verificata. Chiudere il monitor Arduino IDE prima di Upload.
Build non carica il firmware e non prova il touch. Solo il controllo sul dispositivo
conferma il comportamento. Mostrare nel monitor “Consultazione in corso...” e
“Risposta: ...”. Tenere premuto per controllare che non arrivino altre risposte.
Se il collegamento fallisce, consultare examples/CYD.md senza consumare
il resto del talk. Non raccontare questa sessione come riuscita prima di eseguirla.
-->

---

# L’editor aiuta a leggere il progetto

- **Vai alla definizione**: dal richiamo alla funzione
- **Trova riferimenti**: dove viene usata una costante?
- **Problemi**: diagnostica mentre scriviamo
- **Git**: vedere e rivedere le modifiche prima di salvarle nella storia

La compilazione resta il controllo della configurazione effettiva.

<!--
In VSCodium usare F12 su mostraMessaggio e Shift+F12 su ATTESA_RISPOSTA_MS;
mostrare la vista Source Control con una modifica a un testo della risposta.
Un messaggio IntelliSense non è sempre un errore del compilatore: verificare
l’ambiente selezionato e lasciare che PlatformIO ricostruisca l’indice.
Questi strumenti non sono esclusivi di PlatformIO; Arduino IDE 2 include già
funzioni di assistenza al codice. Qui conta usarli su un progetto strutturato.
-->

---

# C++: scegliere anche la toolchain

**Lo sketch Arduino è già C++.**

- Le funzionalità disponibili dipendono da compilatore e libreria standard
- PlatformIO permette di dichiarare le opzioni nel progetto
- Cambiare standard richiede verificare framework e dipendenze

```ini
; Esempio opzionale, non applicato al firmware del benchmark
build_unflags = -std=gnu++11
build_flags = -std=gnu++17
```

<!--
Queste due opzioni sono un esempio per una configurazione che parte da gnu++11;
controllare prima il comando reale con pio run -v. Non copiare senza verificare
quale flag la piattaforma ha impostato. Il compilatore deve supportare lo standard
richiesto e librerie e framework devono restare compatibili.
Arduino IDE non impedisce intrinsecamente il C++ moderno. Nell’Oracolo usiamo
constexpr e tipi espliciti senza cambiare lo standard della configurazione misurata.
Non modificare i flag del benchmark durante questa dimostrazione.
-->

---
layout: center
class: text-center
---

# Cinque minuti di AI: animare l’Oracolo

**Codex integrato in VSCodium · modifica · compilazione · upload**

Dai due cerchi a una sfera animata e luccicante.

<!--
Blocco di circa cinque minuti: mostrare la versione di partenza, inviare il prompt,
seguire le modifiche e la compilazione, quindi osservare il risultato sulla CYD.
Usare Codex già configurato in VSCodium con accesso agli strumenti necessari.
È un aiuto facoltativo: gli esempi si compilano anche senza servizi AI.
Non ripetere la panoramica degli assistenti dell’Arduino Day.
-->

---

# Il prompt per Codex in VSCodium

> voglio una sfera animata lucicante invece di due cerchi, compila e upload in autonomia

- Partenza: copia di `examples/platformio-single-board/`
- Risultato già preparato: `AI-example/`
- Verifica sulla CYD: animazione, tocco e risposta

<!--
Mantenere il prompt nella formulazione scelta dall’utente, incluso «lucicante».
Per la dimostrazione dal vivo lavorare su una copia del progetto iniziale;
AI-example conserva separatamente il codice animato già modificato.
Leggere il diff prodotto da Codex e osservare i comandi di build e upload.
Il prompt richiede autonomia; l’esecuzione dipende da strumenti, permessi e
collegamento della scheda disponibili nella sessione dell’editor.
Verificare sul dispositivo che l’animazione prosegua, che il touch funzioni e
che pressione prolungata, rilascio e nuovo tocco mantengano il comportamento.
La sola compilazione non dimostra fluidità o correttezza su hardware.
-->

---

# Il progetto è pronto da condividere quando…

- Sorgenti e `platformio.ini` sono in Git
- Piattaforma e dipendenze hanno riferimenti espliciti
- Una nuova cartella permette di ricostruire il firmware
- Ogni ambiente dichiarato compila

**Nel repository: esempio Arduino, prima migrazione e misure reali.**

<!--
Stato attuale: i due esempi CYD sono già compilati e verificati sulla scheda
nella preparazione documentata; nessuna seconda scheda è ancora dimostrata.
I workflow esistenti costruiscono le slide e compilano gli esempi Arduino e
PlatformIO. CI non prova display e touch e non esegue il caricamento fisico.
Ricordare che toolchain e dipendenze transitive contano per la riproducibilità.
La prova offline e la registrazione di riserva sono ancora da completare.
-->

---
layout: center
class: text-center
---

# Dallo sketch al progetto

**Lo stesso Oracolo. Più chiaro come ricostruirlo.**

Configurazione in Git · Dipendenze dichiarate · Verifiche ripetibili

Domande?

<div class="benchmark-note">
Materiali: <code>examples/</code> · <code>benchmarks/</code> · <code>notes/sources.md</code><br>
Slide originali: CC BY-SA 4.0 · Codice originale: MIT
</div>

<!--
Chiusura del percorso principale. Riprendere il punto di partenza: abbiamo
mantenuto Arduino come framework e reso esplicita la preparazione del progetto.
Materiali pubblici: https://github.com/fablab-bergamo/linuxday2026-platformio.
-->
