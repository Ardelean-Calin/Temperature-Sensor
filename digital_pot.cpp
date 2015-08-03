#include <Wire.h>
#include <Arduino.h>

void set_pot(uint8_t pot, uint8_t value){
    /*
    value will be the value to write to the potentiometer
    pot will be which pot (either 0 or 1)
    */
    uint8_t address;
    address = pot ? 0xAA : 0xA9; // 0 is A9 and 1 is AA

    Wire.beginTransmission(40);
    Wire.write(address);
    Wire.write(value);
    Wire.endTransmission();
}
