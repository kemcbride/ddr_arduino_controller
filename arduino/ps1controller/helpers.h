#ifndef HELPERS_H
#define HELPERS_H

int Left = 51;
int Right = 50;
int Up = 52;
int Down = 53;
int MacroPin = 10;             // Activation button
int PressDuration = 50; // ms

void press_w_delay(int button_pin, int press_duration, int post_press_delay) {
      digitalWrite(button_pin, LOW);    // Activates button
      delay(press_duration);                 // hold button for duration
      digitalWrite(button_pin, HIGH);    // De-Activates button
      delay(post_press_delay);                  // waits for post press delay
}

void press_button(int button_pin, int press_duration){
      digitalWrite(button_pin, LOW);    // Activates button
      digitalWrite(LED_BUILTIN, HIGH);
      delay(press_duration);                 // hold button for duration
      digitalWrite(button_pin, HIGH);    // De-Activates button
      digitalWrite(LED_BUILTIN, LOW);
}

void press2_button(int button_pin, int button2_pin, int press_duration){
      digitalWrite(button_pin, LOW);    // Activates button
      digitalWrite(button2_pin, LOW);    // Activates button
      digitalWrite(LED_BUILTIN, HIGH);
      delay(press_duration);                 // hold button for duration
      digitalWrite(button_pin, HIGH);    // De-Activates button
      digitalWrite(button2_pin, HIGH);    // Activates button
      digitalWrite(LED_BUILTIN, LOW);
}

void press3_button(int button_pin, int button2_pin, int button3_pin, int press_duration){
      digitalWrite(button_pin, LOW);    // Activates button
      digitalWrite(button2_pin, LOW);    // Activates button
      digitalWrite(button3_pin, LOW);    // Activates button
      digitalWrite(LED_BUILTIN, HIGH);
      delay(press_duration);                 // hold button for duration
      digitalWrite(button_pin, HIGH);    // De-Activates button
      digitalWrite(button2_pin, HIGH);    // Activates button
      digitalWrite(button3_pin, HIGH);    // Activates button
      digitalWrite(LED_BUILTIN, LOW);
}
#endif
