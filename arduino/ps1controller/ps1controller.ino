// PSX DDR Controller Circuit Driven by Arduino Mega
// The idea is that we can generate code in a header file,
// and have this main project import and run the code there,
// and the generated code comes from the .sm files for the exact song.
// Just a cute little exercise to make a circuit that can run 
// the steps from a song, on the press of an activation button.
// Probably, it will need to be recompiled for each song, if I end up doing multiple songs.

#include "helpers.h"  // Shared header containing functions used in per-song files
#include "hysteria.h"

int A = 0;                 // A button connected to digital pin 0
int B = 1;                 // B button connected to digital pin 1
int Select = 2;            // Select button connected to digital pin 2
int Start = 3;             // Start button connected to digital pin 3

void setup()
{
  pinMode(Left, OUTPUT);
  pinMode(Right, OUTPUT); 
  pinMode(Up, OUTPUT); 
  pinMode(Down, OUTPUT); 
  
  pinMode(MacroPin, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);

  int kelly = 100 + bpm;
}


void send_button_presses(){
    /*for (int i = 0; i < 10; ++i) {
      press_w_delay(Right, PressDuration, BetweenPressDelay);
      
      press_w_delay(Up, PressDuration, BetweenPressDelay);

      press_w_delay(Down, PressDuration, BetweenPressDelay);
      
      press_w_delay(Left, PressDuration, BetweenPressDelay);
  }*/
  play_song();
}

void loop()
{
  // digitalWrite(CircleButton, HIGH);       // De-Activates A button
  // digitalWrite(XButton, HIGH);       // De-Activates B button
  // digitalWrite(Select, HIGH);  // De-Activates Select button
  // digitalWrite(Start, HIGH);   // De-Activates Start button
  digitalWrite(Left, HIGH);    // De-Activates Left button
  digitalWrite(Right, HIGH);   // De-Activates Right button 
  digitalWrite(Up, HIGH);      // De-Activates Up button 
  digitalWrite(Down, HIGH);    // De-Activates Down button 
  digitalWrite(MacroPin, HIGH);      // Sets reference HIGH


  int buttonValue = digitalRead(MacroPin);
  if (buttonValue == LOW) {
    send_button_presses();
  }
}
