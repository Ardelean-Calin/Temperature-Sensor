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


# Calculates the temperature of the thermistor given its
# current resistance and its resistance at 25 °C
def get_temperature(resistance=1e+5, rref=1e+5):
    ratio = math.log(resistance / rref)
    # The Steinhart Hart Equation: http://i.imgur.com/WcnzZyT.png
    temperature = A + B * ratio + C * math.pow(ratio, 2) + \
        D * math.pow(ratio, 3)
    # Return the result, in °C with two-digit precision
    return round(math.pow(temperature, -1) - 273.15, 2)


# Calculates the resistance of the thermistor given its
# current temperature and its resistance at 25 °C
#                       or
# Calculater R25 given R and T
#
# input_res is either current measured resistance or R25,
# depending on the case
def get_resistance(temperature, input_res=1e+5, return_ref=False):
    # The Reverse Steinhart Hart Equation: http://i.imgur.com/wiIVNyj.png
    power = _A + _B / temperature + _C / math.pow(temperature, 2)\
        + _D / math.pow(temperature, 3)

    if return_ref is True:
        # Return the resistance at 25 C for calibration purposes
        return round(input_res / math.exp(power))
    else:
        # Return the resistance, in Ω with 0 digit precision (aka integer)
        return round(input_res * math.exp(power))

if __name__ == '__main__':
    result = get_resistance(313.96, 55000, True)
    print(result)
