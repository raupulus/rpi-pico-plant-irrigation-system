from Models.RpiPico import RpiPico
from time import sleep

from machine import Pin

controller = RpiPico(debug=True)
controller.ledOn()

WATER_PUMP = Pin(12, Pin.OUT)
WATER_SENSOR = Pin(8, Pin.IN)

TIMEOUT_WATER_IRRIGATION = 5 # Tiempo de riego en segundos.
SOIL_MOSTURE_SENSOR1_MIN_VOLTAJE = 2 # Valor mínimo de voltaje para activar motor de riego.
SOIL_MOSTURE_SENSOR2_MIN_VOLTAJE = 2 # Valor mínimo de voltaje para activar motor de riego.


def check_water():
    return bool(WATER_SENSOR.value())

def soil_moisture_correct():
    soil_read_1 = controller.readAnalogInput(28)
    #soil_read_2 = controller.readAnalogInput(26)
    #print(soil_read_1, soil_read_2)
    print('Soil 1:', soil_read_1)

    if soil_read_1 > SOIL_MOSTURE_SENSOR2_MIN_VOLTAJE:
        return False

    return True

def water_pump():
    if check_water():
        print('REGANDO')
        WATER_PUMP.value(1)
        sleep(TIMEOUT_WATER_IRRIGATION)
        WATER_PUMP.value(0)
    else:
        print('NO HAY AGUA')


def loop():
    controller.ledOn()

    # Compruebo ambos sensores, en caso de uno faltarle agua activar motor.
    if not soil_moisture_correct():
        water_pump()

    sleep(1)
    controller.ledOff()
    sleep(1)

it = 0

while True:
    try:
        it += 1
        print('Iteración:', it)
        loop()
    except Exception as e:
        print('Error en el loop', e)
        WATER_PUMP.value(0)
