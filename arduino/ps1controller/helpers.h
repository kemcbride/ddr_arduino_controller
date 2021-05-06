#ifndef HELPERS_H
#define HELPERS_H

int Left = 51;              // Left button connected to digital pin 4
int Right = 52;             // Right button connected to digital pin 5
int Up = 50;                // Up button connected to digital pin 6
int Down = 53;              // Down button connected to digital pin 7
int MacroPin = 10;             // Activation button connected to digital pin 10
int PressDuration = 50; // ms
int BetweenPressDelay = 300; // ms


void press_w_delay(int button_pin, int press_duration, int post_press_delay) {
      digitalWrite(button_pin, LOW);    // Activates button
      delay(press_duration);                 // hold button for duration
      digitalWrite(button_pin, HIGH);    // De-Activates button
      delay(post_press_delay);                  // waits for post press delay
}

void press_button(int button_pin, int press_duration){
      digitalWrite(button_pin, LOW);    // Activates button
      delay(press_duration);                 // hold button for duration
      digitalWrite(button_pin, HIGH);    // De-Activates button
}

void press2_button(int button_pin, int button2_pin, int press_duration){
      digitalWrite(button_pin, LOW);    // Activates button
      digitalWrite(button2_pin, LOW);    // Activates button
      delay(press_duration);                 // hold button for duration
      digitalWrite(button_pin, HIGH);    // De-Activates button
      digitalWrite(button2_pin, HIGH);    // Activates button
}

void press3_button(int button_pin, int button2_pin, int button3_pin, int press_duration){
      digitalWrite(button_pin, LOW);    // Activates button
      digitalWrite(button2_pin, LOW);    // Activates button
      digitalWrite(button3_pin, LOW);    // Activates button
      delay(press_duration);                 // hold button for duration
      digitalWrite(button_pin, HIGH);    // De-Activates button
      digitalWrite(button2_pin, HIGH);    // Activates button
      digitalWrite(button3_pin, HIGH);    // Activates button
}
#endif
