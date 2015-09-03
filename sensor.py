import math
import serial
import time

import constants as c
import functions as f


class Sensor:
    gain = 0.0
    vref = 0.0

    def __init__(self, device_path, baudrate=9600, timeout=1):
        self.connection = serial.Serial(device_path, baudrate, timeout=timeout)
        # Wait for connection to be established
        while self.connection.read(1) != b'\n':
            pass
        print("\nConnection established!")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()
        print("\nConnection closed successfully!")

    def _convert(self, voltage, max_value=256):
        """Converts the given voltage to a whole number from 0 to max_value.
        """
        return round(voltage * max_value / c.MAX_VOLTAGE)

    def _convert2(self, value, max_value=256):
        """Converts the given value to a voltage from 0 to 3.3V
        """
        return value * c.MAX_VOLTAGE / max_value

    def _send_command(self, command):
        """Executes command and returns the string representaion of the result.

        First statement converts str to bytes and sends the command.
        Second statement gets the response and decodes it back to a str.

        Commands on the Arduino automatically return an output.
        """
        self.connection.write(command.encode("utf-8"))
        response = self._get_response(self.connection)
        if response == -1:  # Means we timed out. Try again.
            return self._send_command(command)
        return response

    def _get_response(self, connection):
        """Returns a string representation of whatever was sent over serial.

        This method waits until all bytes were read from the serial port.
        Only afterwards does it advance to the next step.
        """
        response = [' ']
        i = 0
        while response[-1] != '\n':
            # Reads byte by byte and converts to characters.
            rbyte = connection.read(1).decode()
            response.append(rbyte)
            # Timeout protection
            if len(rbyte) == 0:
                i += 1
            # If there were more than 1 empty bytes
            # (the first one is always empty I think)
            if i > 1:
                print("Connection timed out. Reconnecting.")
                return -1

        # Join the characters and cut the whitespace and \r \n characters.
        response = ''.join(response)[1:-2]
        return response

    def _read_voltage(self):
        """Returns the voltage at the Analog Sense Pin rounded to 3 decimals.
        """
        command = "o"
        voltage = float(self._send_command(command))
        return round(self._convert2(voltage, max_value=1024), 3)

    def close(self):
        """Closes the serial connection.
        """
        self.connection.close()

    def set_ref_voltage(self, voltage):
        """Sets the voltage of the reference pot and returns the actual voltage.

        We convert the voltage from float to a number from 0 to 255, send that
        value to the pot and read the actual voltage at the pot (0 - 1023).
        We then convert that value to an analog voltage.
        """
        byte_voltage = self._convert(voltage=voltage, max_value=256)
        command = "v 0 {}".format(byte_voltage)
        response = float(self._send_command(command))
        true_voltage = self._convert2(value=response, max_value=1024)

        self.vref = round(true_voltage, 3)
        return self.vref

    def set_gain(self, gain):
        """Sets the gain of the precision amplifier. Returns the actual gain.

        We transform the gain so that we can send it do the digital pot.
        Then we send and return the actual gain which was set.

        Maybe will have to add a way to better measure that gain, must see if
        accurate for now.
        """
        value = math.ceil(256.0/gain) - 1
        command = "v 1 {}".format(value)
        self._send_command(command)

        self.gain = round(256.0/value, 3)
        return self.gain

    def get_temp(self):
        """Returns the temperature of the thermistor in degrees C.
        """
        voltage = self._read_voltage()
        t_voltage = f.get_thermistor_voltage(voltage, self.vref, self.gain)
        res = f.res_from_voltage(t_voltage)
        t = f.temp_from_res(res, rref=c.REFERENCE_RESISTANCE)

        return f.to_celsius(t)

if __name__ == "__main__":
    arduino = Sensor("/dev/ttyUSB0")
    print("Connected!")
    # print(arduino._send_command("o"))
    try:
        # v = arduino._send_command("o")
        v = arduino.set_ref_voltage(1)
        gain = arduino.set_gain(2)
        while True:
            x = arduino.get_temp()
            print(x)
    finally:
        print("Closed")
        arduino.close()
    # print(v)
    # g = arduino.set_gain(1.6231)
    # print(g)
