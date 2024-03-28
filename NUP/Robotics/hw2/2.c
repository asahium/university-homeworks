#define ACTIVE_STATE HIGH
#define INACTIVE_STATE LOW

const int OUTPUT_PINS[] = {
    6, 7, 8, 9, 10}; // Ensure these pins support PWM for analogWrite()
const int INPUT_PINS[] = {2, 3, 4, 5};
int previousMode = 15;

int binaryToDecimal(int binary[], int size) {
  int decimalValue = 0;
  for (int i = 0; i < size; ++i) {
    decimalValue = decimalValue * 2 + binary[i];
  }
  return decimalValue;
}

void switchOffAll() {
  for (int pin : OUTPUT_PINS) {
    digitalWrite(pin, INACTIVE_STATE);
  }
}

// New function for Pulse Wave effect
void pulseWave(int pulseDelay) {
  // Gradually increase brightness
  for (int brightness = 0; brightness <= 255; brightness++) {
    for (int pin : OUTPUT_PINS) {
      analogWrite(pin, brightness);
    }
    delay(pulseDelay);
  }
  // Gradually decrease brightness
  for (int brightness = 255; brightness >= 0; brightness--) {
    for (int pin : OUTPUT_PINS) {
      analogWrite(pin, brightness);
    }
    delay(pulseDelay);
  }
}

void setup() {
  Serial.begin(9600);
  for (int pin : OUTPUT_PINS) {
    pinMode(pin, OUTPUT);
  }
  for (int pin : INPUT_PINS) {
    pinMode(pin, INPUT_PULLUP);
  }
}

void loop() {
  int switchPinSize = sizeof(INPUT_PINS) / sizeof(INPUT_PINS[0]);
  int pinsValues[switchPinSize];
  for (int i = 0; i < switchPinSize; ++i) {
    pinsValues[i] = digitalRead(INPUT_PINS[i]);
  }
  int mode = binaryToDecimal(pinsValues, switchPinSize);
  if (mode != previousMode) {
    switchOffAll();
    previousMode = mode;
  }

  // Adjust pulseDelay based on the mode to control the speed of the pulsing
  // effect
  int pulseDelay = 0; // Time in milliseconds for delay in pulseWave function
  switch (mode) {
  case 14:
    pulseDelay = 5; // Faster pulsing
    break;
  case 13:
    pulseDelay = 10;
    break;
  case 11:
    pulseDelay = 20;
    break;
  case 7:
    pulseDelay = 40; // Slower pulsing
    break;
  default:
    pulseDelay = 15; // Default speed
    break;
  }
  pulseWave(pulseDelay);
}
