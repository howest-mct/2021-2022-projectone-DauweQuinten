from helpers.i2c_LCD import i2c_LCD
from RPi import GPIO
import time

rs_pin = 24
E_pin = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(rs_pin, GPIO.OUT)
GPIO.setup(E_pin, GPIO.OUT)

lcd = i2c_LCD(0x20, rs_pin, E_pin)


lcd.init_LCD()
lcd.write_message("Hello World!")

try:
    while True:
        time.sleep(0.2)
except KeyboardInterrupt:
    print("programma gestopt")
finally:
    lcd.shutdown()
    GPIO.cleanup()
