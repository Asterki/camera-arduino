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
const int buttonPin = 2;

MD_Parola P = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);
int buttonState = 0;  // variable for reading the pushbutton status

void setup() {
  P.begin();
  P.setIntensity(0);
  P.displayClear();
  pinMode(buttonPin, INPUT);
}

void loop() {
  P.setTextAlignment(PA_CENTER);
  P.setFont(newFont);
  
  buttonState = digitalRead(buttonPin);

  if (buttonState == HIGH) {
    P.print("3");
    delay(2000);

    P.print("2");
    delay(2000);

    P.print("1");
    delay(2000);

    P.print("!");
    delay(2000);
  } else {
    P.displayClear();
  }
}