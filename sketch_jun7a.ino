#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>
#include "Parola_Fonts_data.h"

// Uncomment according to your hardware type
#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
//#define HARDWARE_TYPE MD_MAX72XX::GENERIC_HW

// Defining size, and output pins
#define MAX_DEVICES 2
#define CS_PIN 5

MD_Parola P = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);

void setup() {
  P.begin();
  P.setIntensity(0);
  P.displayClear();
}

void loop() {
  P.setTextAlignment(PA_CENTER);
  P.setFont(newFont);
  
  P.print("1");
  delay(2000);

  P.print("2");
  delay(2000);

  P.print("3");
  delay(2000);
}