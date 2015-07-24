#ifndef DIGITAL_POT_H
#define DIGITAL_POT_H

#include <Arduino.h>

const int TPIN = A0;  // op-amp output pot. senses temperature
const int POT_0 = A1; // sense pin of pot 0
const int POT_1 = A2; // sense pin of pot 1

void set_pot(uint8_t pot, uint8_t value);
int read_pot(int sense_pin);

#endif
