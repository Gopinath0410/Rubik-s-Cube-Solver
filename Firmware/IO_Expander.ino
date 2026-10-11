// PCF8575 output state
// 1 = HIGH
// 0 = LOW
uint16_t pcfState = 0xFFFF;

void writePCF8575(uint16_t data)
{
  Wire.beginTransmission(PCF8575_ADDR);

  // Low byte first
  Wire.write(data & 0xFF);

  // High byte
  Wire.write((data >> 8) & 0xFF);

  byte error = Wire.endTransmission();

  if (error == 0)
  {
    pcfState = data;

    Serial.print("PCF8575 = 0x");
    Serial.println(pcfState, HEX);
  }
  else
  {
    Serial.print("I2C ERROR = ");
    Serial.println(error);
  }
}

void setPort(uint8_t port, bool state)
{
  if (port > 15)
  {
    Serial.println("Invalid port. Use P0 to P15.");
    return;
  }

  if (state)
    pcfState |= (1 << port);      // HIGH
  else
    pcfState &= ~(1 << port);     // LOW

  writePCF8575(pcfState);

  // Serial.print("P");
  // Serial.print(port);
  // Serial.print(" = ");
  // Serial.println(state ? "HIGH" : "LOW");
}