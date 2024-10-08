#include <MD_Parola.h>
#include <MD_MAX72xx.h>
#include <SPI.h>
#include "Parola_Fonts_data.h" // The custom font so that it shows sideways

// Uncomment according to your hardware type
#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
//#define HARDWARE_TYPE MD_MAX72XX::GENERIC_HW

// Defining size, and output pins
#define MAX_DEVICES 2

const int buttonPin = 2;
#define CLK_PIN   23        // Changed for ESP32 in Wokwi
#define DATA_PIN  19        // Changed for ESP32 in Wokwi
#define CS_PIN    22        // Changed for ESP32 in Wokwi

// Changed from hardware to software for ESP32 in Wokwi
// HARDWARE SPI
// MD_Parola P = MD_Parola(HARDWARE_TYPE, CS_PIN, MAX_DEVICES);
// SOFTWARE SPI
MD_Parola P = MD_Parola(HARDWARE_TYPE, DATA_PIN, CLK_PIN, CS_PIN, MAX_DEVICES);
int buttonState = 0;  // variable for reading the pushbutton status

void setup() {
  Serial.begin(9600);
  P.begin();
  P.setIntensity(0);
  P.displayClear();
  pinMode(buttonPin, INPUT);
}

void loop() {
  P.setTextAlignment(PA_CENTER);
  P.setFont(newFont);
  
  buttonState = digitalRead(buttonPin);

  // When the button is pressed, start the countdown
  if (buttonState == HIGH) {
    Serial.println("Button pressed");
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