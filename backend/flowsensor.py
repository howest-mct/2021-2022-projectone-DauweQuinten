from RPi import GPIO
import time

flowsens = 20
pulsen = 0


def flow_puls_callback(pin):
    print("puls detected")
    global pulsen
    pulsen += 1
    print(pulsen)


GPIO.setmode(GPIO.BCM)

GPIO.setup(flowsens, GPIO.IN, GPIO.PUD_DOWN)

GPIO.add_event_detect(flowsens, GPIO.RISING,
                      flow_puls_callback, bouncetime=100)


try:
    while True:
        time.sleep(0.2)


except KeyboardInterrupt:
    print("programma gestopt")
finally:
    GPIO.cleanup()
