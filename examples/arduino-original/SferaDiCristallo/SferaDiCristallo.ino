// SPDX-License-Identifier: MIT
// Esempio originale per Linux Day 2026, FabLab Bergamo.
// Destinazione: CYD ESP32-2432S028R con ILI9341 e touch XPT2046.
#include <SPI.h>
#include <Adafruit_GFX.h>
#include <Adafruit_ILI9341.h>
#include <XPT2046_Touchscreen.h>
#include <esp_system.h>

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
  schermo.drawCircle(160, 100, 30, ILI9341_CYAN);
  schermo.drawCircle(160, 100, 27, ILI9341_WHITE);
  schermo.drawFastHLine(125, 134, 70, ILI9341_CYAN);
}

void mostraMessaggio(const char* messaggio, const char* istruzione) {
  disegnaCornice();
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

  mostraMessaggio("Fai una domanda...", "Poi tocca lo schermo");
  digitalWrite(RETROILLUMINAZIONE, HIGH);
  Serial.println("Sfera pronta: tocca lo schermo per una risposta.");
}

void loop() {
  const uint32_t adesso = millis();
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
