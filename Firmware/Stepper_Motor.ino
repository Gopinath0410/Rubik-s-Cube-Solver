

void rotateMotor(Motor &m, bool direction, int steps)
{
  digitalWrite(m.dirPin, direction);

  delayMicroseconds(100);

  Serial.print("Rotating ");
  Serial.print(m.name);
  Serial.print(" - ");
  Serial.print(steps);
  Serial.println(" steps");

  for (int i = 0; i < steps; i++)
  {
    digitalWrite(m.stepPin, HIGH);
    delayMicroseconds(STEP_DELAY_US);



    digitalWrite(m.stepPin, LOW);
    delayMicroseconds(STEP_DELAY_US);
  }

  Serial.println("Rotation complete");
}

void disableAllMotors(){
  writePCF8575(0xFFFF);
}