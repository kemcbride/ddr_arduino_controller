// PSX DDR Controller Circuit Driven by Arduino Mega
// The idea is that we can generate code in a header file,
// and have this main project import and run the code there,
// and the generated code comes from the .sm files for the exact song.
// Just a cute little exercise to make a circuit that can run 
// the steps from a song, on the press of an activation button.
// Probably, it will need to be recompiled for each song, if I end up doing multiple songs.

#include "helpers.h"  // Shared header containing functions used in per-song files
#include "letthemmove.h"

void setup()
{
  pinMode(Left, OUTPUT);
  pinMode(Right, OUTPUT); 
  pinMode(Up, OUTPUT); 
  pinMode(Down, OUTPUT); 
  
  pinMode(MacroPin, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop()
{
  // digitalWrite(CircleButton, HIGH);
  // digitalWrite(XButton, HIGH);
  // digitalWrite(Select, HIGH);
  // digitalWrite(Start, HIGH);
  digitalWrite(Left, HIGH);
  digitalWrite(Right, HIGH);
  digitalWrite(Up, HIGH);
  digitalWrite(Down, HIGH);
  digitalWrite(MacroPin, HIGH);      // Sets reference HIGH

 int buttonValue = digitalRead(MacroPin);
 if (buttonValue == LOW) {
    play_song();
  }
}
