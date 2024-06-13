import pyfirmata

comport = 'COM5'

board = pyfirmata.Arduino(comport)

led_green = board.get_pin('d:8:o')
led_red = board.get_pin('d:9:o')
alarm = board.get_pin('d:10:o')

def led(gesture):
    if gesture == 'rock':
        led_green.write(1)
        led_red.write(0)
        alarm.write(0)
    elif gesture == 'paper':
        led_green.write(0)
        led_red.write(1)
        alarm.write(0)
    elif gesture == 'scissor':
        led_green.write(0)
        led_red.write(0)
        alarm.write(1)
    else:
        led_green.write(0)
        led_red.write(0)
        alarm.write(0)
