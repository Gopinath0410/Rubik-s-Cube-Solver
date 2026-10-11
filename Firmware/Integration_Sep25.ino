
/******************************************************
 * Project: Automatic Rubik's cube solver
 * Author: Gopinath.G
 * Firmware Version:"REV_1.0_INDEV"
 * Release Date: Oct-2026
 * Contact information:query.gopi@gmail.com
 * ------------------------------------------
 * Hardware:
 *   - ESP32
 *   -A4988 Stepper Motor drivers
 ******************************************************/
#include <Wire.h>

#define PCF8575_ADDR 0x27

#define SDA_PIN 21
#define SCL_PIN 22

#define STEP_DELAY_US 50

#define STEP_pulse 800

// =====================================================
// MOTOR STRUCTURE
// =====================================================

struct Motor
{
  const char* name;
  uint8_t stepPin;
  uint8_t dirPin;
  uint8_t enablePin;
};

Motor motors[] =
{
  // Name     STEP   DIR   PCF
  {"UP",       32,   33,    0},
  {"BACK",     25,   26,    1},
  {"DOWN",     27,   23,    2},
  {"LEFT",     13,   19,    3},
  {"FRONT",    18,   17,    4},
  {"RIGHT",    16,    4,    5}
};

const int NUM_MOTORS = sizeof(motors) / sizeof(motors[0]);

void setup()
{
  Serial.begin(115200);

  Wire.begin(SDA_PIN, SCL_PIN);

  delay(500);

  // Start with all ports HIGH
  
  //writePCF8575(0x0000);
// Configure STEP and DIR pins  2
  for (int i = 0; i < NUM_MOTORS; i++)
  {
    pinMode(motors[i].stepPin, OUTPUT);
    pinMode(motors[i].dirPin, OUTPUT);

    digitalWrite(motors[i].stepPin, LOW);
    digitalWrite(motors[i].dirPin, LOW);
  }

  delay(500);
disableAllMotors();

 //writePCF8575(0xFFFF);//All ports ON tends to disable all stepers.
 //writePCF8575(0x0000);//All ports Off tends to enable all stepers.
    
}

void loop()
{
  input_data();
  
}