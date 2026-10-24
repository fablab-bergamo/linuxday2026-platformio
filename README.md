# Linux Day 2026 · Bergamo

Slide in italiano sul passaggio da Arduino IDE a PlatformIO, realizzate con Markdown e Slidev.
Il punto di partenza è [slides.md](slides.md). La presentazione è ancora una bozza. Gli esempi della [Sfera di cristallo](examples/README.md) sono disponibili per Arduino IDE e PlatformIO, con istruzioni e stato delle verifiche sulla scheda. I [tempi di compilazione misurati](benchmarks/README.md) sono conservati con metodo, versioni e risultati grezzi per le slide.

Percorso previsto: piccolo progetto ESP32, migrazione tramite interfaccia grafica VSCodium/PlatformIO e aiuto mirato dell’AI. Gli esempi funzionano sulla Cheap Yellow Display con ILI9341 e touch resistivo XPT2046; resta da annotare la sigla esatta del PCB e la revisione. La scaletta didattica è descritta in [notes/outline.md](notes/outline.md).

## Riprendere il lavoro

Stato al 24 ottobre 2026:

- Repository GitHub **pubblico**: https://github.com/fablab-bergamo/linuxday2026-platformio.
- Entrambi gli esempi della Sfera di cristallo sono compilati e provati sulla stessa scheda, con conferma dell’utente per display, touch e pressione prolungata. Sulla scheda è caricata la versione Arduino IDE.
- Arduino IDE 1.8.19 e PlatformIO Core 6.2.0 usano Arduino-ESP32 2.0.14 e le stesse versioni delle librerie. La [guida CYD](examples/CYD.md) documenta pin, dipendenze, installazione e problemi risolti su Linux.
- Le [misure di compilazione Linux e Windows](benchmarks/README.md) sono complete: 18 compilazioni riuscite per macchina, tre prove per scenario. I CSV restano separati; le slide mostrano le colonne Linux e Windows, con i due motori in ogni cella. Su Windows, dopo una piccola modifica, le mediane sono 14,89 s con Arduino Builder e 9,77 s con PlatformIO. Il [wrapper](benchmarks/run-windows.ps1) permette di ripetere la sessione con strumenti dedicati e percorsi brevi.
- `slides.md` contiene 26 slide in italiano, con note del relatore: migrazione guidata in VSCodium, codice importato dal firmware, dipendenze, benchmark Linux e Windows, configurazione C++, ambienti hardware ed esercizio AI di circa cinque minuti. La seconda scheda è solo uno schema didattico: il progetto eseguibile con più ambienti, la registrazione di riserva e la prova completa offline restano da preparare.
- Le 26 slide attuali sono state compilate ed esportate in PDF con successo su Linux. Le slide aggiornate sono state controllate visivamente durante la revisione. È fissata `floating-vue` 5.2.2 per eliminare un errore di inizializzazione con Slidev 52.6.0. HTML e PDF generati restano esclusi da Git.

Alla prossima sessione:

1. Eseguire `git status`, poi avviare la presentazione con i comandi sotto.
2. Rivedere le slide e le note seguendo `notes/outline.md`, mostrando codice importato dagli esempi eseguibili quando pratico.
3. Mantenere separati i dati Linux e Windows nelle slide e mostrare metodo e intervalli. Le misure escludono download, interfacce grafiche e upload; non misurano la velocità del firmware.
4. Scegliere la seconda scheda e preparare gli ambienti PlatformIO, esplicitando le differenze hardware.
5. Provare dal vivo l’esercizio AI già descritto nelle slide, preparare la registrazione di riserva e una prova offline; ricontrollare HTML e PDF dopo gli aggiornamenti.

Per installazione e risoluzione dei problemi consultare la guida CYD. La prova completa offline resta da effettuare. I benchmark pubblici omettono metadati personali e dettagli dei computer ospiti.

## Installazione

Usare Node.js 22, almeno versione 22.12.0. Se nvm è installato:

```sh
nvm use
npm ci
npm run dev
```

Aprire http://localhost:3030. Le modifiche vengono visualizzate automaticamente. La vista relatore è disponibile su http://localhost:3030/presenter.
Separare le slide con `---` e scrivere le note del relatore nei commenti HTML.

Le dipendenze sono installate e `package-lock.json` è incluso nel repository. Usare `npm ci` per riprodurre le versioni registrate: attualmente Slidev 52.6.0, tema predefinito 0.25.0 e Playwright Chromium 1.56.1.

## Compilazione ed esportazione

```sh
npm run build
npm run setup:browser
npm run export
```

Il sito HTML viene generato in `dist/`; il PDF in `slides-export.pdf`. Entrambi sono esclusi da Git.
L’esportazione usa Playwright Chromium. Su Linux, eventuali dipendenze di sistema mancanti possono essere installate con `npx playwright install --with-deps chromium`, che può richiedere privilegi di amministratore.

Per vedere il sito compilato, eseguire `python3 -m http.server 8080 --directory dist` e aprire http://localhost:8080. La base relativa permette di ospitare il sito anche in un sottopercorso. `routerMode: hash` mantiene la navigazione all’interno di quel percorso (ad esempio `/linuxday2026-platformio/#/5`): GitHub Pages non fornisce il fallback necessario alle rotte HTML5. Dopo modifiche alla pubblicazione, verificare su un server statico in un sottopercorso l’apertura dell’indice, la selezione touch di una slide e il ricaricamento del relativo URL.

## Verifiche e integrazione continua

GitHub Actions è configurato per compilare il sito, esportare il PDF e conservare entrambi come artefatti. Non pubblica il sito. Un secondo workflow compila gli esempi ESP32 e la variante animata `AI-example`, con PlatformIO e Arduino CLI.

Prima dell’evento, controllare leggibilità e impaginazione di HTML e PDF. Installare dipendenze e Chromium in anticipo, quindi fare una prova senza connessione. Il caricamento remoto dei caratteri è disabilitato; il funzionamento offline deve ancora essere verificato.

## Struttura

- `slides.md`: slide e note del relatore.
- `notes/outline.md`: scaletta e scelte didattiche.
- `notes/sources.md`: fonti, attribuzioni e verifiche pendenti.
- `examples/`: versioni Arduino IDE e PlatformIO, istruzioni CYD e prove su hardware.
- `AI-example/`: variante animata già preparata per la dimostrazione con Codex in VSCodium.
- `benchmarks/`: metodo, tabella, misure grezze e script per ripeterle.
- `AGENTS.md`: istruzioni di lavoro per gli assistenti.

## Licenze

Le slide e le note originali sono distribuite con licenza [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
Configurazione, strumenti ed esempi originali sono distribuiti con licenza MIT: vedere [LICENSE](LICENSE). Le dipendenze e i materiali esterni mantengono le proprie licenze. Prima di riutilizzare materiale del Libro dei progetti, verificarne la licenza specifica.

## Presentazione online

La presentazione è disponibile su [GitHub Pages](https://fablab-bergamo.github.io/linuxday2026-platformio/). Il workflow `.github/workflows/slides.yml` compila HTML ed esporta il PDF; sui push al ramo `main` pubblica `dist/` con GitHub Pages. Le pull request eseguono solo le verifiche. Il PDF è scaricabile dagli artefatti del workflow. È possibile avviare il workflow anche manualmente da GitHub Actions. Nelle impostazioni della repository, Pages deve usare **GitHub Actions** come sorgente.
