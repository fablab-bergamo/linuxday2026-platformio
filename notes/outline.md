# Scaletta del talk

Tutto il materiale deve essere in italiano. Ipotesi di lavoro: 35–40 minuti di contenuto più domande; durata da confermare. Preparare anche un percorso ridotto a 30 minuti.

## Decisioni e proposte

- Pubblico: utilizzatori di Arduino IDE; piccolo esempio didattico ESP32.
- Interfaccia principale: VSCodium con PlatformIO, usando i comandi grafici.
- Scheda preferita: Cheap Yellow Display, indicata dall’utente con un budget di circa 15 euro su AliExpress. Modello esatto e revisione da confermare; candidata ESP32-2432S028R da 2,8 pollici. In alternativa, un’altra ESP32.
- Esempio scelto: Sfera di cristallo, ispirata al progetto 11 del Libro dei progetti segnalato dal FabLab. Adattamento con risposta sul display e attivazione tramite touch, senza rete o sensori esterni.
- Preparare prima la versione Arduino IDE sulla stessa scheda e con lo stesso comportamento; migrare poi solo l’ambiente di sviluppo. L’adattamento hardware dal libro è un passaggio separato.
- Usare una grafica semplice: non introdurre LVGL o editor di interfacce durante questa dimostrazione.

## Tempi

| Minuti | Contenuto |
| --- | --- |
| 4 | Progetto funzionante e motivazioni per cambiare ambiente |
| 4 | Editor, PlatformIO, framework Arduino e compilatore |
| 12 | Creazione progetto, migrazione, dipendenze, compilazione, caricamento e monitor seriale |
| 7 | Versioni delle librerie, tempi misurati, navigazione e seconda configurazione hardware |
| 5 | AI: diagnosi di un errore specifico della migrazione e verifica della correzione |
| 3 | Lista di controllo, limiti e risorse |

Per la versione da 30 minuti ridurre il confronto dei vantaggi e mostrare la seconda configurazione come modifica già preparata.

## Evitare sovrapposizioni con Arduino Day 2026

Il resoconto del precedente talk descrive generazione di sketch da linguaggio naturale, chatbot, agenti nell’editor e da terminale, test e versioning. Il PDF è stato individuato ma non è stato possibile leggerlo: il confronto si basa sul resoconto.

Non ripetere una panoramica degli assistenti o una dimostrazione di generazione di un nuovo progetto. Qui l’AI interviene su una migrazione già spiegata: legge file e diagnostica un errore concreto. I lavori di Andreas Spiess servono come riferimento per il ciclo compilazione–verifica, senza introdurre il suo intero banco di prova.

## Verifiche ancora necessarie

Display, touch e caricamento sono stati verificati in entrambi gli ambienti, con conferma dell’utente. Gli esempi originali sono in `examples/arduino-original` e `examples/platformio-single-board`; non riproducono codice o immagini del libro. Le misure confrontabili sono salvate in `benchmarks/README.md` e `benchmarks/results.csv` e sono inserite nelle slide. Restano da annotare sigla e revisione del PCB, scegliere la seconda scheda, preparare una registrazione di riserva e completare la prova offline. Il README contiene il punto di ripartenza.

## Nucleo narrativo: libertà e dipendenze

Dedicare circa 8–10 minuti, inclusa la dimostrazione, al passaggio dalle installazioni del computer alle dipendenze dichiarate nel progetto. Questa parte rientra nei tempi di migrazione e librerie già previsti, non si somma al totale.

1. Motivazione: rendere espliciti strumenti e configurazione del progetto; distinguere editor, piattaforma, SDK e toolchain.
2. Problema: aggiornare una libreria condivisa nello sketchbook può cambiare più sketch. Mostrare il beneficio di versioni diverse per progetto.
3. Libertà della sorgente: registro, Git, fork, archivi e cartelle. La compatibilità resta da verificare.
4. Caso reale: importare il platformio.ini dell’Oracolo; display dal registro e touch da un commit ufficiale. Spiegare come condividere anche una correzione non pubblicata nel catalogo.
5. Verifica: compilare e controllare il comportamento. Poi mostrare i benchmark registrati, separando il beneficio organizzativo dai tempi misurati.

Confronto corretto: Arduino IDE accetta anche ZIP e installazioni manuali; Arduino CLI offre installazione Git e profili sketch.yaml isolati. Presentare l’integrazione di queste operazioni nel flusso PlatformIO, senza attribuirgli possibilità esclusive.

## Passaggio dall’ambiente didattico all’editor

Prima della presentazione di PlatformIO, confrontare Arduino IDE e VSCodium: partire rapidamente con uno sketch, poi organizzare un progetto hobbistico che cresce nel tempo. Distinguere editor, strumenti di compilazione e framework. Evitare l’obbligo implicito di cambiare per qualunque hobby: il beneficio emerge con più file, dipendenze, revisioni e strumenti. La nuova slide non cambia lo stato delle prove: il flusso grafico completo su VSCodium resta da verificare.

## Completamento del percorso nelle slide

Dopo dipendenze e benchmark, la dimostrazione segue queste tappe:

1. Aprire la cartella PlatformIO in VSCodium; distinguere src, include, lib e .pio.
2. Confrontare sketch e main.cpp: Arduino.h e dichiarazioni prima delle chiamate. Importare il codice reale nelle slide.
3. Eseguire Build, Upload e Monitor da Project Tasks. Verificare tocco, attesa, rilascio e risposta sul dispositivo.
4. Mostrare navigazione, diagnostica e standard C++: il supporto dipende da compilatore, librerie e framework.
5. Spiegare ambienti comuni e specifici. La seconda ESP32 DevKit è solo un esempio di configurazione: scheda fisica ancora da scegliere, nessun nuovo pin configurato.
6. Cinque minuti di AI: errore intenzionale di dichiarazione in una copia, diagnosi, lettura della modifica e compilazione. Caso preparato, non una sessione già registrata.
7. Chiudere con checklist e risorse. Per problemi di upload e preparazione offline, consultare la documentazione del repository.

Percorso da 30 minuti: sintetizzare storia e catalogo delle piattaforme, abbreviare il confronto degli editor. Nessuna nuova verifica hardware o offline è implicita nelle slide aggiunte.
