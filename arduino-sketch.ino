#include <Event.h>
#include <EEPROM.h>
#include "Timer.h"
#include <stdio.h>

const int TPIN = A0;

int samplesPerRead  = 2;    // number of samples per read

const byte STRLEN = 255;    // maximum length of a command
char commandString[STRLEN]; // the string containing the full command
char command; // only the command

Timer t;
int sampleEvent, stopEvent;

void setup(){
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

            case 's': // sample
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

            case 'c': // config internal variables (maybe even reference voltage and gain?)
                sscanf(commandString, "%*s %d", &samplesPerRead);
                Serial.println(samplesPerRead);
                break;

            case 'v': // set reference voltage

                break;

            case 'o': // one-time sample and return
                sample_data();
                break;

            case 'h': // halt
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
    // Send serial data to know that I've stopped
}