#!/usr/bin/env python3

import math

# Steinhart Hart Coefficients for determining temperature
A = 3.354016e-3
B = 2.460382e-4
C = 3.405377e-6
D = 1.034240e-7

# Steinhart Hart Coefficients for determining resistance
_A = -16.0349
_B = 5459.339
_C = -191141
_D = -3328322


# Converts from Kelvin to Celsius with given precision
def to_celsius(temperature, precision=2):
    return round(temperature - 273.15, precision)


# Converts from Celsius to Kelvin with given precision
def to_kelvin(temperature, precision=2):
    return round(temperature + 273.15, precision)


# Calculates the temperature of the thermistor given its
# current resistance and its resistance at 25 °C
def get_temperature(resistance=1e+5, rref=1e+5):
    ratio = math.log(resistance / rref)
    # The Steinhart Hart Equation: http://i.imgur.com/WcnzZyT.png
    temperature = A + B * ratio + C * math.pow(ratio, 2) + \
        D * math.pow(ratio, 3)
    # Flip it over
    temperature = math.pow(temperature, -1)
    # Return the result, in °C with two-digit precision
    return to_celsius(temperature)


# The Reverse Steinhart Hart Equation: http://i.imgur.com/wiIVNyj.png

# Calculates the resistance of the thermistor given its
# current temperature and its resistance at 25 °C
def get_resistance(temperature, reference_resistance=1e+5):
    e_pow = _A + _B / temperature + _C / math.pow(temperature, 2)\
        + _D / math.pow(temperature, 3)

    return round(reference_resistance * math.exp(e_pow))


# Get the resistance at 25 C according to the current temperature (K)
# and resistance (ohm)
def get_reference_resistance(temperature, resistance):
    e_pow = _A + _B / temperature + _C / math.pow(temperature, 2)\
        + _D / math.pow(temperature, 3)

    return round(resistance / math.exp(e_pow))

if __name__ == '__main__':
    print(get_temperature(81720))
    print(get_temperature(82720))
    print("hello world!")
    # result = get_resistance(to_kelvin(21.97), 100000)
    # print(result)
