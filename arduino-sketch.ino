#include <Event.h>
#include <EEPROM.h>
#include "Timer.h"
#include <stdio.h>

const int TPIN = A0;

byte samplesPerRead  = 2;    // number of samples per read

const byte STRLEN = 255;    // maximum length of a command
char commandString[STRLEN]; // the string containing the full command
char command; // only the command

Timer t;
int sampleEvent, stopEvent;

void setup(){
    // Step 1: load configuration from EEPROM
    //load_config();
    // Step 2: setup serial communication
    Serial.begin(9600); // Seems like on the 8MHz this is actually 4800 baud
    Serial.println("Ready");
}


// Appearantly readUntil doesn't have the 64 character limitation
String inputData;
void loop(){
    // Enter command mode and listen to commands.
    // Depending on the command, execute the instructions given
    if (Serial.available() > 0){
        // My command
        Serial.readBytesUntil('\n', commandString, STRLEN);
        // Command is "s 250 20" or "sample 250 20"
        Serial.println(commandString);
        command = commandString[0];
        switch (command) {
            case 's':
                long stopTime; // int would mean max 31s
                long delayBetweenSamples; // int would mean max 31s

                sscanf(commandString, "%*s %ld %ld", &stopTime, &delayBetweenSamples);

                Serial.println(stopTime);
                Serial.println(delayBetweenSamples);
                // arguments:
                // stopTime, delayBetweenSamples
                // runs sample_data every x microseconds
                sampleEvent = t.every(delayBetweenSamples, sample_data);
                // Stops all timers after the given time
                stopEvent   = t.after(stopTime, stop_timers); // will maybe take 1 less sample than expected.
              break;
            case 'h':
              stop_timers();

              break;
            default:
                Serial.println("Command invalid!");
        }
    }
    while(Serial.read() != -1); // clear the serial buffer

    for(int i=0; i<STRLEN; i++) // clear my string
        commandString[i] = 0;

    t.update();
}


// Takes samplesPerRead samples and averages them to eliminate noise
// instantly sends the data to the PC
void sample_data(){
    // float sampleValue = 0.0;
    // // Samples X times in one go. Eg 20 times
    // for(int i=0; i<samplesPerRead; i++)
    //     sampleValue += analogRead(TPIN);
    // sampleValue /= samplesPerRead;

    Serial.println("Sampling!");

    // !!! Send data through serial !!!
    // Serial.write(sampleValue);
}


// Stops all timers
void stop_timers(){
    Serial.println("Stopped timers");
    t.stop(sampleEvent);
    t.stop(stopEvent);
}

// Loads the configuration variables from EEPROM. These are:
// samples per read - address 0         (1 byte)
// resistance at 25 C - address 1-5     (4 bytes)
void load_config(){
    EEPROM.get(0, samplesPerRead); // read from address 0
    //EEPROM.get(1, refResistance);  // read from address 1
}


// Saves current global values to EEPROM
// Since the EEPROM has about 100 000 write/erase cycles
// updating writes to the EEPROM only if the value has
// changed, therefor not using erase cycles when unnecessary
// put() can put any data type into memory.
void save_config(){
    EEPROM.put(0, samplesPerRead); // samples at address 0
    //EEPROM.put(1, refResistance);  // R25 at address 1-5 (4 bytes)
}