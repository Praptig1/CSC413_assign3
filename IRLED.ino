#include <IRremote.hpp>

// Pin definitions
#define IR_RECEIVE_PIN 2
#define GREEN_PIN 10
#define RED_PIN 11
#define BLUE_PIN 12

// Define button codes
#define BUTTON_FORWARD 0xF609FF00  // Replace with your "Forward" button code
#define BUTTON_BACK 0xF807FF00     // Replace with your "Back" button code
#define BUTTON_PLUS 0xBF40FF00     // Replace with your "+" button code
#define BUTTON_MINUS 0xE619FF00    // Replace with your "-" button code
#define BUTTON_ENTER 0xEA15FF00

void setup() {
  IrReceiver.begin(IR_RECEIVE_PIN, ENABLE_LED_FEEDBACK); // Start IR receiver with LED feedback
  pinMode(RED_PIN, OUTPUT);
  pinMode(GREEN_PIN, OUTPUT);
  pinMode(BLUE_PIN, OUTPUT);

  Serial.begin(9600); // // Establish serial communication
}

void loop() {
  if (IrReceiver.decode()) {
    unsigned long code = IrReceiver.decodedIRData.decodedRawData; // Get raw button code
    if (code == BUTTON_FORWARD) {
      Serial.println("NEXT");
      activateLED(BLUE_PIN);
    } else if (code == BUTTON_BACK) {
      Serial.println("PREVIOUS");
      activateLED(BLUE_PIN);
    } else if (code == BUTTON_PLUS) {
      Serial.println("FAVORITE");
      activateLED(GREEN_PIN);
    } else if (code == BUTTON_MINUS) {
      Serial.println("DELETE");
      activateLED(RED_PIN);
    } else if (code == BUTTON_ENTER) {
      Serial.println("ENTER");
    }

    IrReceiver.resume(); // Enable receiving of the next value
  }
}

// Function to activate an LED for 1 second
void activateLED(int pin) {
  digitalWrite(pin, HIGH);
  if (pin == BLUE_PIN) {
    delay(200);
  } else {
    delay(500);
  }
  digitalWrite(pin, LOW);
}
