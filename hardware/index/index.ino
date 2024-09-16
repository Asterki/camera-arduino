#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>
#include "Parola_Fonts_data.h"
#include <Firmata.h>

#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 2
#define CS_PIN 5
const int buttonPin = 13;

MD_Parola P = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);
int buttonState = 0;
int lastValue = LOW;

void setup() {
  P.begin();
  P.setIntensity(0);
  P.displayClear();
  pinMode(buttonPin, INPUT);
  Firmata.setFirmwareVersion(FIRMATA_FIRMWARE_MAJOR_VERSION, FIRMATA_FIRMWARE_MINOR_VERSION);
  Firmata.begin(57600);
}

void loop() {
  while (Firmata.available()) {
    Firmata.processInput();
  }

  int value = digitalRead(buttonPin);

  if (value != lastValue && value == HIGH) {
    Firmata.sendDigital(buttonPin, value);
  }

  lastValue = value;

  buttonState = digitalRead(buttonPin);

  if (buttonState == HIGH) {
    P.setTextAlignment(PA_CENTER);
    P.setFont(newFont);
    
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
