#include <stdio.h>
#include <Wire.h>

#include "digital_pot.h"

const byte STRLEN = 255;    // maximum length of a command

int samplesPerRead  = 20;   // number of samples per read

char commandString[STRLEN]; // the string containing the full command
char command;               // only the command's first character


void setup(){
    // Step 2: setup serial communication
    Serial.begin(9600); // Seems like on the 8MHz this is actually 4800 baud
    Wire.begin();       // Start i2c communication as Master
    Serial.println("Ready");
}


void loop(){
    if (Serial.available() > 0){
        // My command
        Serial.readBytesUntil('\n', commandString, STRLEN);
        command = commandString[0];

        switch (command) {

            case 'c': // config samplesPerRead
                sscanf(commandString, "%*s %d", &samplesPerRead);
                break;

            case 'v': // voltage pot[0-1] value[0-255]
                int pot;
                int voltage;

                sscanf(commandString, "%*s %d %d", &pot, &voltage);
                set_pot(pot, voltage);
                break;

            case 'o': // one-time-sample
                sample_data(TPIN);
                break;

            case 'r':
                int pin_to_read;

                sscanf(commandString, "%*s %d", &pin_to_read);
                sample_data(pin_to_read);
                break;

            default:
                Serial.write("Command invalid!");
        }
    }


    while(Serial.read() != -1); // clear the serial buffer

    for(int i=0; i<STRLEN; i++)
        commandString[i] = 0;
}


// Takes samplesPerRead samples and averages them to eliminate noise
// instantly sends the data to the PC
void sample_data(int pin){
    float sampleValue = 0.0;
    // Samples X times in one go. Eg 20 times
    for(int i=0; i<samplesPerRead; i++)
        sampleValue += analogRead(pin);
    sampleValue /= samplesPerRead;

    Serial.println(sampleValue);

    // !!! Send data through serial !!!
    // Serial.write(sampleValue);
}
