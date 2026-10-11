int steps;

int findMotor(String name)
{
  for (int i = 0; i < NUM_MOTORS; i++)
  {
    if (name == motors[i].name)
      return i;
  }

  return -1;
}

void input_data()
{
  if (Serial.available())
  {
    String command = Serial.readStringUntil('\n');

    command.trim();
    command.toUpperCase();

    if (command.length() == 0)
      return;

    Serial.print("Received sequence: ");
    Serial.println(command);

    // =====================================================
    // PROCESS SEQUENCE
    // =====================================================

    int start = 0;

    while (start < command.length())
    {
      // Skip spaces
      while (start < command.length() &&
             command.charAt(start) == ' ')
      {
        start++;
      }

      if (start >= command.length())
        break;

      // ===================================================
      // GET MOVE LETTER
      // ===================================================

      char move = command.charAt(start);

      // Check valid move
      if (move != 'U' &&
          move != 'D' &&
          move != 'L' &&
          move != 'R' &&
          move != 'F' &&
          move != 'B')
      {
        Serial.print("Invalid move: ");
        Serial.println(move);

        // Move to next token
        while (start < command.length() &&
               command.charAt(start) != ' ')
        {
          start++;
        }

        continue;
      }

      start++;

      // ===================================================
      // DEFAULT
      // ===================================================

      bool direction = HIGH;
      int rotationSteps = STEP_pulse;

      // ===================================================
      // CHECK ' OR 2
      // ===================================================

      if (start < command.length())
      {
        char modifier = command.charAt(start);

        // -----------------------------------------------
        // PRIME MOVE
        // Example: L'
        // -----------------------------------------------

        if (modifier == '\'')
        {
          direction = LOW;
          rotationSteps = STEP_pulse;

          start++;
        }

        // -----------------------------------------------
        // DOUBLE MOVE
        // Example: U2
        // -----------------------------------------------

        else if (modifier == '2')
        {
          direction = HIGH;
          rotationSteps = STEP_pulse * 2;

          start++;
        }
      }

      // ===================================================
      // FIND MOTOR NAME
      // ===================================================

      String motorName;

      switch (move)
      {
        case 'U':
          motorName = "UP";
          break;

        case 'D':
          motorName = "DOWN";
          break;

        case 'L':
          motorName = "LEFT";
          break;

        case 'R':
          motorName = "RIGHT";
          break;

        case 'F':
          motorName = "FRONT";
          break;

        case 'B':
          motorName = "BACK";
          break;
      }

      // ===================================================
      // FIND MOTOR
      // ===================================================

      int motorIndex = findMotor(motorName);

      if (motorIndex == -1)
      {
        Serial.print("Motor not found: ");
        Serial.println(motorName);
        continue;
      }

      // ===================================================
      // DISPLAY MOVE
      // ===================================================

      Serial.print("Executing: ");
      Serial.print(move);

      if (direction == LOW)
        Serial.print("'");

      else if (rotationSteps == STEP_pulse * 2)
        Serial.print("2");

      Serial.print(" -> ");
      Serial.print(motorName);

      Serial.print(" -> ");
      Serial.print(rotationSteps);
      Serial.println(" steps");

      // ===================================================
      // DISABLE ALL MOTORS
      // ===================================================

      disableAllMotors();

      // ===================================================
      // ENABLE ONLY SELECTED MOTOR
      // ===================================================

      setPort(motorIndex, LOW);

      delay(50);

      // ===================================================
      // ROTATE
      // ===================================================

      rotateMotor(
        motors[motorIndex],
        direction,
        rotationSteps
      );

      // ===================================================
      // DISABLE AFTER ROTATION
      // ===================================================

      delay(50);

      disableAllMotors();

      delay(50);
    }

    Serial.println("================================");
    Serial.println("Sequence complete");
    Serial.println("================================");
  }
}