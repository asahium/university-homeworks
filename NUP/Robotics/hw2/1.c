// Macro definitions for readability
#define ACTIVE_STATE HIGH
#define INACTIVE_STATE LOW

// Pin assignments
const int OUTPUT_PIN_SET[] = {6, 7, 8, 9, 10};
const int INPUT_PIN_SET[] = {2, 3, 4, 5};
const int RGB_PINS[] = {11, 12, 13}; // Assuming for RGB LED control

// Global state
int lastMode = -1;

// Convert binary array to decimal
int binaryToDecimal(int *binary, int length) {
  int decimal = 0;
  for (int i = 0; i < length; i++) {
    decimal = (decimal << 1) | binary[i];
  }
  return decimal;
}

// Turn off all specified output pins
void deactivateAllPins() {
  for (int pin : OUTPUT_PIN_SET) {
    digitalWrite(pin, INACTIVE_STATE);
  }
  for (int pin : RGB_PINS) {
    digitalWrite(pin, INACTIVE_STATE);
  }
}

// Activate all output pins continuously
void activateAllPins() {
  for (int pin : OUTPUT_PIN_SET) {
    digitalWrite(pin, ACTIVE_STATE);
  }
}

// Sequentially activate output pins
void sequentialActivation() {
  for (int pin : OUTPUT_PIN_SET) {
    digitalWrite(pin, ACTIVE_STATE);
    delay(100); // Timing delay for visual effect
    digitalWrite(pin, INACTIVE_STATE);
  }
}

// Adjust RGB LED color based on offset
void adjustRGBColor(int offset) {
  int red = sin(offset + 0) * 127 + 128;
  int green = sin(offset + 2) * 127 + 128;
  int blue = sin(offset + 4) * 127 + 128;

  analogWrite(RGB_PINS[0], red);
  analogWrite(RGB_PINS[1], green);
  analogWrite(RGB_PINS[2], blue);
}

// Display a binary counter on the output pins
void displayBinaryCounter(int count) {
  for (size_t i = 0; i < sizeof(OUTPUT_PIN_SET) / sizeof(OUTPUT_PIN_SET[0]);
       i++) {
    int state = (count >> i) & 1;
    digitalWrite(OUTPUT_PIN_SET[i], state ? ACTIVE_STATE : INACTIVE_STATE);
  }
  delay(350);
}

void setup() {
  Serial.begin(9600);
  for (int pin : OUTPUT_PIN_SET) {
    pinMode(pin, OUTPUT);
  }
  for (int pin : RGB_PINS) {
    pinMode(pin, OUTPUT);
  }
  for (int pin : INPUT_PIN_SET) {
    pinMode(pin, INPUT_PULLUP);
  }
}

void loop() {
  int modeSwitchCount = sizeof(INPUT_PIN_SET) / sizeof(INPUT_PIN_SET[0]);
  int modeSwitchValues[modeSwitchCount];
  for (int i = 0; i < modeSwitchCount; i++) {
    modeSwitchValues[i] = digitalRead(INPUT_PIN_SET[i]);
  }
  int currentMode = binaryToDecimal(modeSwitchValues, modeSwitchCount);

  if (currentMode != lastMode) {
    deactivateAllPins();
    lastMode = currentMode;
  }

  switch (currentMode) {
  case 14:
    activateAllPins();
    break;
  case 13:
    sequentialActivation();
    break;
  case 12:
    for (int offset = 0; offset < 36; offset++) {
      adjustRGBColor(offset);
      delay(70);
    }
    break;
  case 11:
  case 7:
    int count = (currentMode == 11) ? 0 : 31;
    do {
      displayBinaryCounter(count);
      count = (currentMode == 11) ? (count + 1) % 32 : (count - 1 + 32) % 32;
      if (currentMode == 11)
        Serial.print(count);
    } while (count != 0);
    break;
  }
}
