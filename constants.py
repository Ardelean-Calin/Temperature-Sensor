import configparser


config = configparser.ConfigParser()

MAX_CMD_LENGTH = 0
SERIES_RESISTANCE = 0
MAX_VOLTAGE = 0
REFERENCE_RESISTANCE = 0
SAVE_LOCATION = ""


def load_config():
    config.read('config.conf')

    sensor_config = config['temperature_sensor']
    # global keyword is needed in order to WRITE to a global variable
    global MAX_CMD_LENGTH
    global SERIES_RESISTANCE
    global MAX_VOLTAGE
    global REFERENCE_RESISTANCE
    global SAVE_LOCATION

    MAX_CMD_LENGTH = int(sensor_config['max_cmd_length'])
    SERIES_RESISTANCE = int(sensor_config['series_resistance'])
    MAX_VOLTAGE = float(sensor_config['max_voltage'])
    REFERENCE_RESISTANCE = float(sensor_config['reference_resistance'])
    SAVE_LOCATION = sensor_config['save_location']


def set_constant(constant_name, value):
    """constant_name is the same string as in the config file
    and value can be the real type, it will be converted to string.
    """
    config['temperature_sensor'][constant_name] = str(value)
    with open('config.conf', 'w') as configfile:
        config.write(configfile)
    load_config()


load_config()
