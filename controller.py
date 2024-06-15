import pyfirmata

comport = 'COM5'

board = pyfirmata.Arduino(comport)

led_green = board.get_pin('d:8:o')
led_red = board.get_pin('d:9:o')
led_yellow = board.get_pin('d:10:o')

gestur_terakhir = None

def led(gestur):
    global gestur_terakhir

    if gestur != 'nohand':
        gestur_terakhir = gestur

    if gestur_terakhir == 'rock':
        led_green.write(1)
        led_red.write(0)
        led_yellow.write(0)
    elif gestur_terakhir == 'paper':
        led_green.write(0)
        led_red.write(1)
        led_yellow.write(0)
    elif gestur_terakhir == 'scissors':
        led_green.write(0)
        led_red.write(0)
        led_yellow.write(1)
    elif gestur_terakhir == 'off':
        led_green.write(0)
        led_red.write(0)
        led_yellow.write(0)
    # else:
    #     led_green.write(0)
    #     led_red.write(0)
    #     led_yellow.write(0)

# Turn off function
def turn_off():
    led_green.write(0)
    led_red.write(0)
    led_yellow.write(0)
