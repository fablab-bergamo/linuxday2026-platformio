// SPDX-License-Identifier: MIT
// Esempio originale per Linux Day 2026, FabLab Bergamo.
// Destinazione: CYD ESP32-2432S028R con ILI9341 e touch XPT2046.
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>
#include <XPT2046_Touchscreen.h>
#include <esp_system.h>
#include <math.h>

// Display e touch usano due bus SPI distinti sulla CYD classica.
constexpr uint8_t DISPLAY_MISO = 12;
constexpr uint8_t DISPLAY_MOSI = 13;
constexpr uint8_t DISPLAY_CLK = 14;
constexpr uint8_t DISPLAY_CS = 15;
constexpr uint8_t DISPLAY_DC = 2;
constexpr uint8_t RETROILLUMINAZIONE = 21;
constexpr uint8_t TOUCH_MISO = 39;
constexpr uint8_t TOUCH_MOSI = 32;
constexpr uint8_t TOUCH_CLK = 25;
constexpr uint8_t TOUCH_CS = 33;

constexpr uint32_t ATTESA_RISPOSTA_MS = 800;
constexpr uint32_t FILTRO_TOCCO_MS = 50;
const char* const RISPOSTE[] = {
  "Direi proprio di si!",
  "Meglio aspettare.",
  "Prova un'altra strada.",
  "Le stelle dicono no.",
  "Ottime prospettive!",
  "Chiedimelo di nuovo.",
  "Serve un esperimento.",
  "Il futuro e' aperto."
};
constexpr size_t NUMERO_RISPOSTE = sizeof(RISPOSTE) / sizeof(RISPOSTE[0]);

SPIClass busDisplay(HSPI);
SPIClass busTouch(VSPI);
Adafruit_ILI9341 schermo(&busDisplay, DISPLAY_DC, DISPLAY_CS, -1);
// Lettura senza interrupt: non servono coordinate o calibrazione del touch.
XPT2046_Touchscreen touch(TOUCH_CS);

bool toccoLetto = false;
bool toccoStabile = false;
bool inAttesa = false;
uint32_t ultimoCambioTocco = 0;
uint32_t inizioAttesa = 0;
constexpr int SFERA_L = 112;
constexpr int SFERA_H = 108;
constexpr int RAGGIO = 42;
constexpr uint32_t FRAME_MS = 40;
GFXcanvas16 sfera(SFERA_L, SFERA_H);
uint32_t ultimoFrame = 0;
float faseSfera = 0.0f;

void animaSfera(uint32_t adesso) {
  const uint32_t trascorso = adesso - ultimoFrame;
  if (trascorso < FRAME_MS || !sfera.getBuffer()) return;
  ultimoFrame = adesso;
  faseSfera += fminf(trascorso, 100) * (inAttesa ? 0.0045f : 0.0015f);
  sfera.fillScreen(ILI9341_NAVY);
  // Alone morbido e volume illuminato dall'alto a sinistra.
  for (int y = 3; y <= 95; ++y) {
    for (int x = 10; x <= 102; ++x) {
      const float nx = (x - 56) / float(RAGGIO);
      const float ny = (y - 49) / float(RAGGIO);
      const float r2 = nx * nx + ny * ny;
      if (r2 > 1.20f) continue;
      float rosso, verde, blu;
      if (r2 > 1.0f) {
        const float alone = (1.20f - r2) * 5.0f;
        rosso = 10 * alone;
        verde = 48 * alone;
        blu = 128 + 65 * alone;
      } else {
        const float z = sqrtf(1.0f - r2);
        const float luce = fmaxf(0, -0.42f * nx - 0.55f * ny + 0.72f * z);
        const float bordo = powf(1.0f - z, 3);
        const float nube = 0.5f + 0.5f * sinf(8 * nx + 5 * ny + faseSfera +
                                               2 * sinf(5 * ny - faseSfera));
        const float riflesso = expf(-((nx + 0.36f) * (nx + 0.36f) * 45 +
                                      (ny + 0.48f) * (ny + 0.48f) * 85));
        rosso = 12 + 38 * luce + 42 * nube * z + 80 * bordo + 160 * riflesso;
        verde = 24 + 95 * luce + 45 * nube * z + 95 * bordo + 150 * riflesso;
        blu = 90 + 105 * luce + 40 * nube * z + 60 * bordo + 100 * riflesso;
      }
      sfera.drawPixel(x, y, schermo.color565(uint8_t(fminf(255, rosso)),
                         uint8_t(fminf(255, verde)), uint8_t(fminf(255, blu))));
    }
  }
  sfera.fillRoundRect(28, 96, 56, 7, 3, 0x31AC);
  sfera.drawFastHLine(32, 96, 48, ILI9341_CYAN);
  // Piccoli riflessi a stella pulsano in punti diversi del cristallo.
  for (int i = 0; i < 7; ++i) {
    const float angolo = i * 2.39996f + faseSfera * 0.18f;
    const float distanza = 17 + (i % 3) * 10;
    const int x = 56 + cosf(angolo) * distanza;
    const int y = 49 + sinf(angolo) * distanza;
    const float intensita = powf(fmaxf(0, sinf(faseSfera * 2.4f + i * 1.7f)), 4);
    if (intensita < 0.12f) continue;
    const uint16_t colore = schermo.color565(100 + 155 * intensita,
                                             170 + 85 * intensita, 255);
    const int braccio = 1 + int(3 * intensita);
    sfera.drawFastHLine(x - braccio, y, 2 * braccio + 1, colore);
    sfera.drawFastVLine(x, y - braccio, 2 * braccio + 1, colore);
    sfera.drawPixel(x, y, ILI9341_WHITE);
  }
  schermo.drawRGBBitmap(104, 40, sfera.getBuffer(), SFERA_L, SFERA_H);
}

void scriviCentrato(const char* testo, int16_t y, uint8_t dimensione,
                    uint16_t colore) {
  int16_t xTesto, yTesto;
  uint16_t larghezza, altezza;
  schermo.setTextSize(dimensione);
  schermo.setTextColor(colore);
  schermo.getTextBounds(testo, 0, 0, &xTesto, &yTesto, &larghezza, &altezza);
  schermo.setCursor((schermo.width() - larghezza) / 2 - xTesto, y);
  schermo.print(testo);
}

void disegnaCornice() {
  schermo.fillScreen(ILI9341_NAVY);
  scriviCentrato("SFERA DI CRISTALLO", 18, 2, ILI9341_YELLOW);
}

void mostraMessaggio(const char* messaggio, const char* istruzione) {
  schermo.fillRect(0, 150, schermo.width(), 90, ILI9341_NAVY);
  scriviCentrato(messaggio, 156, 2, ILI9341_WHITE);
  scriviCentrato(istruzione, 214, 1, ILI9341_CYAN);
}

void setup() {
  Serial.begin(115200);
  pinMode(RETROILLUMINAZIONE, OUTPUT);
  digitalWrite(RETROILLUMINAZIONE, LOW);

  busDisplay.begin(DISPLAY_CLK, DISPLAY_MISO, DISPLAY_MOSI, DISPLAY_CS);
  schermo.begin(20000000);
  schermo.setRotation(1);
  schermo.setTextWrap(false);

  busTouch.begin(TOUCH_CLK, TOUCH_MISO, TOUCH_MOSI, TOUCH_CS);
  touch.begin(busTouch);

  disegnaCornice();
  mostraMessaggio("Fai una domanda...", "Poi tocca lo schermo");
  ultimoFrame = millis() - FRAME_MS;
  animaSfera(millis());
  digitalWrite(RETROILLUMINAZIONE, HIGH);
  Serial.println("Sfera pronta: tocca lo schermo per una risposta.");
}

void loop() {
  const uint32_t adesso = millis();
  animaSfera(adesso);
  const bool premuto = touch.touched();

  // Conferma pressione e rilascio solo dopo un breve intervallo stabile.
  if (premuto != toccoLetto) {
    toccoLetto = premuto;
    ultimoCambioTocco = adesso;
  }
  if (toccoLetto != toccoStabile &&
      adesso - ultimoCambioTocco >= FILTRO_TOCCO_MS) {
    toccoStabile = toccoLetto;
    if (toccoStabile && !inAttesa) {
      inAttesa = true;
      inizioAttesa = adesso;
      mostraMessaggio("Sto consultando...", "Attendi la risposta");
      Serial.println("Consultazione in corso...");
    }
  }

  // Nessun delay: il touch continua a essere letto durante l'attesa.
  if (inAttesa && adesso - inizioAttesa >= ATTESA_RISPOSTA_MS) {
    inAttesa = false;
    const size_t indice = esp_random() % NUMERO_RISPOSTE;
    mostraMessaggio(RISPOSTE[indice], "Rilascia e tocca per riprovare");
    Serial.print("Risposta: ");
    Serial.println(RISPOSTE[indice]);
  }
}
