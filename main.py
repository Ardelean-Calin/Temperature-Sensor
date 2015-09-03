#!/usr/bin/python3
import math
import matplotlib.pyplot as plt
import numpy as np
import os
import subprocess
import sys
import time

import constants as c
import functions as f
import sensor

port = None


def get_serial_port():

    serial_ports = subprocess.check_output(
        "python3 -m serial.tools.list_ports",
        shell=True).decode().split("\n")

    for port in serial_ports:
        if "ttyUSB" in port:
            return port.strip()  # removes trailing whitespace


def show_help():
    # I'll show the arguments and how to use the program
    print("God help you.")
    sys.exit(0)


def measure(vref, gain, duration, delay, file_name):

    # I need to also consider the first measurment at t = 0
    max_iterations = math.ceil(duration / delay) + 1
    data = np.zeros(shape=(max_iterations, 2))  # array full of 0's

    plt.ion()  # turn interactive mode on
    plt.draw()

    with sensor.Sensor(port, baudrate=9600, timeout=1) as arduino:
        arduino.set_gain(gain)
        arduino.set_ref_voltage(vref)

        print("Initialization complete! Starting measurements.")

        i = 0  # counts the number of measurments taken
        # I do this once at t = 0s
        temperature = arduino.get_temp()
        save_to_file(file_name, i * delay, temperature)
        data[i] = [i * delay, temperature]

        print(data[i])  # prints the time and temperature

        add_to_plot(data)

        i += 1
        # Then I do it every "delay" seconds
        t_prev = time.time()

        while True:
            t_now = time.time()

            if t_now - t_prev >= delay:
                t_prev = t_now

                temperature = arduino.get_temp()
                save_to_file(file_name, i * delay, temperature)

                data[i] = [i * delay, temperature]  # add row to matrix

                print(data[i])

                add_to_plot(data)

                i += 1

                if i >= max_iterations:
                    break

    plt.title("Measurment complete.")
    print("Measurments done! There were ", i, " measurements.")


# Appends the (preferably formated) data to a text file
def save_to_file(file_name, time, data):
    if file_name.endswith(".txt") is False:
        file_name += ".txt"

    with open(c.SAVE_LOCATION + file_name, "a") as f:
        f.write("{}\t{}\n".format(time, data))


# Data is a pair of time, temperature
def add_to_plot(data):
    plt.cla()  # clear axes
    plt.title("Ongoing measurment")
    plt.ylim(float(sys.argv[2]), float(sys.argv[3]))
    plt.scatter(data[:, 0], data[:, 1])
    plt.draw()


# Checks if file exists and prompt to remove or not.
def check_if_file_exists(filename):
    if filename.endswith(".txt") is False:
        filename += ".txt"

    if os.path.isfile(c.SAVE_LOCATION + filename):
        print("File", filename, "already exists.",
              "Should I overwrite it? [y/N]")
        answer = input().upper()

        if answer == 'Y':
            os.remove(c.SAVE_LOCATION + filename)


def main():
    if len(sys.argv) < 2:
        print("Unsufficient parameters. Try again. ")
        print("Example: ./main.py measure 10 40 25m30s 10s simulare")
        sys.exit(0)
    command = sys.argv[1]

    if command == "help":
        show_help()

    elif command == "calibrate":
        pass

    elif command == "measure":
        # These are mandatory parameters
        min_temp = f.to_kelvin(float(sys.argv[2]))
        max_temp = f.to_kelvin(float(sys.argv[3]))
        duration = f.extract_time(sys.argv[4])
        delay = f.extract_time(sys.argv[5])
        # This is not
        try:
            title = sys.argv[6]
        except IndexError:
            title = time.strftime("%H_%M_%S", time.localtime()) + ".txt"
            print("Name of savefile not found. Using", title, "as the name.")
        check_if_file_exists(title)
        # Map basically executes the given functions with each parameter
        max_res, min_res = map(f.res_from_temp, (min_temp, max_temp))
        min_voltage, max_voltage = map(f.voltage_from_res, (min_res, max_res))

        vref = min_voltage
        gain = f.gain_from_voltage(min_voltage, max_voltage)

        measure(vref, gain, duration, delay, title)

    else:
        print("This command does not exist. Try again!")
        sys.exit(0)

if __name__ == "__main__":
    try:
        port = get_serial_port()
        if port is None:
            print("Sensor not detected. Try again!")
            sys.exit(0)
        # I also tell how much the execution took
        then = time.time()
        main()
        now = time.time()
        print("Total time: {:.2f}s".format(now - then))
        print("Press CTRL+C or close the plot window in order to exit.")

        plt.ioff()
        plt.show()

    except KeyboardInterrupt:
        print("\nGoodbye!")
        sys.exit(0)
