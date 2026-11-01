# Repository guidance

## Purpose

Create slides and runnable demonstrations for Linux Day 2026 in Bergamo about moving from Arduino IDE to PlatformIO. The audience is familiar with Arduino sketches but may be new to PlatformIO and structured C++ projects.

Explain migration through one small project that develops progressively. Cover compilation speed, language and tooling configuration, AI-assisted development, dependency management, and development across multiple boards. Keep the Arduino framework during the initial migration so that the audience can follow one change at a time.

## Presentation workflow

- Use Slidev with Markdown, Git, and a local browser preview. The scaffold provides development, build, and PDF export scripts; install dependencies before running them.
- Write the outline and speaker notes before investing in visual customization. A 30–40 minute talk is a planning assumption, not a confirmed duration.
- Keep slides concise, readable on a projector, and centered on concrete examples. Put deeper explanations in speaker notes.
- Prefer built-in Slidev features and a simple, consistent theme over custom Vue components.
- Keep assets and fonts local so the built presentation works without an internet connection.
- Support a static HTML presentation and a PDF handout. Review PDF output because interactive elements may not carry over.
- Write all slides, speaker notes, documentation, and new explanatory code comments in Italian, as explicitly requested by the user. Keep commands, filenames, API names, and license texts unchanged.
- Prefer a graphical VS Code/PlatformIO walkthrough with a small ESP32 teaching example. The preferred hardware is a Cheap Yellow Display; confirm its exact model before implementing pin or display configuration.
- Avoid repeating the Arduino Day 2026 AI overview. Keep AI focused on migration assistance, for approximately five minutes.

## Intended layout

```text
slides.md                          Main presentation and speaker notes
public/                            Local images, fonts, and demo recordings
examples/arduino-original/         Original Arduino sketch
examples/platformio-single-board/  First migration
examples/platformio-multi-board/   Multiple board environments
benchmarks/README.md               Measurement method, hardware, and versions
benchmarks/results.csv             Recorded measurements
notes/outline.md                   Narrative and timing
notes/sources.md                   Technical references and asset attribution
README.md                          Obiettivi didattici, contenuti e materiali
```

Create directories as needed rather than adding empty placeholders. Keep runnable examples as the source of truth for code shown in slides; use Slidev file imports where practical.

## Technical accuracy

- Demonstrate advantages through working code and measured results, not blanket claims.
- Compare clean builds, unchanged rebuilds, and rebuilds after a small edit using comparable boards, toolchains, settings, and dependency state. Record the method and versions; do not invent benchmark results or promise universal speedups.
- Explain that modern C++ support depends on the selected toolchain and board. Arduino IDE does not inherently prevent using modern language features.
- Show explicit dependency declarations in `platformio.ini`; pin demonstrated dependencies and platform versions when practical for reproducibility.
- Use multiple PlatformIO environments to demonstrate board configuration. Explain any hardware abstractions or library compatibility constraints instead of implying automatic portability.
- Present AI assistance as an optional editor or CLI workflow. Validate generated changes with builds and relevant checks; do not imply AI integration is exclusive to PlatformIO.
- Cite primary documentation for technical claims and keep references in `notes/sources.md`.

## Development and validation

- Once scaffolded, provide and document `npm run dev`, `npm run build`, and `npm run export`. Commit the package lockfile and document the supported Node version.
- Build the HTML deck and export the PDF after substantive slide or theme changes. Inspect affected slides for clipping, contrast, and readable code.
- Compile affected PlatformIO examples and, when available, all demonstrated board environments before release. Distinguish successful compilation from checks performed on physical hardware.
- Add meaningful tests for demonstration logic when useful; do not add tests that merely mirror slide content or configuration.
- Configure CI to build the deck, export the PDF, and compile demonstration environments once the corresponding projects exist.
- Keep generated builds, dependency directories, and PlatformIO build caches out of version control.
- Prepare cached toolchains and dependencies plus local recordings for an offline rehearsal. Do not claim offline readiness until it has been checked.
- Publishing and external communications require user authorization; building local artifacts is part of normal development.

## Licensing

Use CC BY-SA 4.0 for original slide content and MIT for original example code, as proposed in the project discussion. Clearly document the scope of each license when adding license files. Preserve third-party licenses and attribution; use appropriately licensed assets. The authoring, build, and presentation workflow must remain usable without paid services or AI tools.

## Guida operativa della presentazione

### Installazione

Usare Node.js 22, almeno versione 22.12.0. Se nvm è installato:

```sh
nvm use
npm ci
npm run dev
```

Aprire http://localhost:3030. Le modifiche vengono visualizzate automaticamente. La vista relatore è disponibile su http://localhost:3030/presenter.
Separare le slide con `---` e scrivere le note del relatore nei commenti HTML.

Le dipendenze sono installate e `package-lock.json` è incluso nel repository. Usare `npm ci` per riprodurre le versioni registrate: attualmente Slidev 52.6.0, tema predefinito 0.25.0 e Playwright Chromium 1.56.1.

### Compilazione ed esportazione

```sh
npm run build
npm run setup:browser
npm run export
```

Il sito HTML viene generato in `dist/`; il PDF in `slides-export.pdf`. Entrambi sono esclusi da Git.
L’esportazione usa Playwright Chromium. Su Linux, eventuali dipendenze di sistema mancanti possono essere installate con `npx playwright install --with-deps chromium`, che può richiedere privilegi di amministratore.

Per vedere il sito compilato, eseguire `python3 -m http.server 8080 --directory dist` e aprire http://localhost:8080. La base relativa permette di ospitare il sito anche in un sottopercorso. `routerMode: hash` mantiene la navigazione all’interno di quel percorso (ad esempio `/linuxday2026-platformio/#/5`): GitHub Pages non fornisce il fallback necessario alle rotte HTML5. Dopo modifiche alla pubblicazione, verificare su un server statico in un sottopercorso l’apertura dell’indice, la selezione touch di una slide e il ricaricamento del relativo URL.

### Verifiche e integrazione continua

GitHub Actions è configurato per compilare il sito, esportare il PDF e conservare entrambi come artefatti. Sui push a `main` pubblica inoltre il sito con GitHub Pages. Un secondo workflow compila gli esempi ESP32 e la variante animata `examples/AI-example`, con PlatformIO e Arduino CLI.

Prima dell’evento, controllare leggibilità e impaginazione di HTML e PDF. Installare dipendenze e Chromium in anticipo, quindi fare una prova senza connessione. Il caricamento remoto dei caratteri è disabilitato; il funzionamento offline deve ancora essere verificato.

### Pubblicazione configurata

La presentazione è disponibile su [GitHub Pages](https://fablab-bergamo.github.io/linuxday2026-platformio/). Il workflow `.github/workflows/slides.yml` compila HTML ed esporta il PDF; sui push al ramo `main` pubblica `dist/` con GitHub Pages. Le pull request eseguono solo le verifiche. Il PDF è scaricabile dagli artefatti del workflow. È possibile avviare il workflow anche manualmente da GitHub Actions. Nelle impostazioni della repository, Pages deve usare **GitHub Actions** come sorgente.
