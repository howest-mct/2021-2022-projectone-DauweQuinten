from RPi import GPIO
import time


GPIO.setmode(GPIO.BCM)
GPIO.setup(21, GPIO.OUT)


try:
    while True:
        GPIO.output(21, 1)
        time.sleep(3)
        GPIO.output(21, 0)
        time.sleep(3)
except KeyboardInterrupt:
    print("programma gestopt")
finally:
    GPIO.output(21, 0)
    GPIO.cleanup()
