import time
import math
import onewire
import ds18x20
from machine import ADC, Pin, I2C
from pico_lcd import I2cLcd
from picozero import Speaker
time.sleep(0.1)

alarme = Speaker(0)
ledR = Pin(2, Pin.OUT)
ledG = Pin(3, Pin.OUT)
ledB = Pin(4, Pin.OUT)

display = I2C(0, sda=Pin(20), scl=Pin(21), freq=400000)
gasInfo = I2cLcd(display, 0x21, 2, 16)
gasMinMax = I2cLcd(display, 0x20, 2, 16)
luzInfo = I2cLcd(display, 0x22, 2, 16)
luzMinMax = I2cLcd(display, 0x23, 2, 16)
tempInfo = I2cLcd(display, 0x26, 2, 16)
tempMinMax = I2cLcd(display, 0x25, 2, 16)
portaInfo = I2cLcd(display, 0x27, 2, 16)

# Mude os Minímos e Máximos dependendo da sua necessidade
gas = ADC(Pin(28))
gasMin = 1000
gasMax = 25000
gasEstavel = False

luz = ADC(Pin(27))
luzMin = 30
luzMax = 75
luzEstavel = False

temp = ds18x20.DS18X20(onewire.OneWire(Pin(22)))
sensorTemp = temp.scan()
tempMin = 15
tempMax = 35
tempEstavel = False

porta = Pin(18, Pin.IN)
portaFechada = False

def Gas():
    global gasEstavel

    gasInfo.clear()
    gasInfo.move_to(0, 0)
    gasMinMax.clear()
    gasMinMax.move_to(0, 0)

    gasMinMax.putstr(f"Gas Max: {gasMax}ppm")
    gasMinMax.move_to(0, 1)
    gasMinMax.putstr(f"Gas Min: {gasMin}ppm")

    valorGas = max(13475, min(64655, gas.read_u16()))
    valorGas = 0.1 * ((3.863451 / ((65535 - valorGas) / valorGas)) ** 2.44589)

    gasInfo.putstr(f"Gas: {valorGas:.0f}ppm")

    if valorGas >= gasMin and valorGas <= gasMax:
        gasEstavel = True
    else:
        gasEstavel = False
        gasInfo.move_to(0, 1)
        gasInfo.putstr("X" * 16)


def Luz():
    global luzEstavel

    luzInfo.clear()
    luzInfo.move_to(0, 0)
    luzMinMax.clear()
    luzMinMax.move_to(0, 0)

    luzMinMax.putstr(f"Luz Max: {luzMax}%")
    luzMinMax.move_to(0, 1)
    luzMinMax.putstr(f"luz Min: {luzMin}%")

    valorLuz = ((luz.read_u16() * 100) / 65007) * -1 + 101

    luzInfo.putstr(f"Luz: {valorLuz:.0f}%")

    if valorLuz >= luzMin and valorLuz <= luzMax:
        luzEstavel = True
    else:
        luzEstavel = False
        luzInfo.move_to(0, 1)
        luzInfo.putstr(f"x" * 16)

def Temperatura():
    global tempEstavel

    tempInfo.clear()
    tempInfo.move_to(0, 0)
    tempMinMax.clear()
    tempMinMax.move_to(0, 0)

    tempMinMax.putstr(f"Temp Max: {tempMax}c")
    tempMinMax.move_to(0, 1)
    tempMinMax.putstr(f"Temp Min: {tempMin}c")

    valorTemp = 0
    for t in sensorTemp:
        valorTemp = temp.read_temp(t)

    tempInfo.putstr(f"Temp: {valorTemp:.0f}c")

    if valorTemp >= tempMin and valorTemp <= tempMax:
        tempEstavel = True
    else:
        tempEstavel = False
        tempInfo.move_to(0, 1)
        tempInfo.putstr("x" * 16)

def Porta():
    global portaFechada

    portaInfo.clear()
    portaInfo.move_to(0,0)

    if porta.value() == 1:
        portaFechada = True
        portaInfo.putstr("Porta Fechada")
    else:
        portaFechada = False
        portaInfo.putstr("Porta Aberta")
        portaInfo.move_to(0,1)
        portaInfo.putstr("X" * 16)

def Verificacao():
    estado = "Normal"

    if (not luzEstavel and not tempEstavel) or not gasEstavel or not portaFechada:
        estado = "Emergencia"
    elif not luzEstavel or not tempEstavel:
        estado = "Alerta"
    else:
        estado = "Normal"

    if estado == "Normal":
        ledR.value(1)
        ledG.value(0)
        ledB.value(1)
    elif estado == "Alerta":
        ledR.value(0)
        ledG.value(0)
        ledB.value(1)
    else:
        ledR.value(0)
        ledG.value(1)
        ledB.value(1)


    if estado == "Emergencia":
        alarme.play("c2")
    else:
        alarme.off()
    
    print(f"Estado: {estado}")


while True:
    try:
        temp.convert_temp()
        time.sleep(1)

        Gas()
        Luz()
        Temperatura()
        Porta()

        Verificacao()
    except:
        print("")
