from RPi import GPIO
import time

flowsens = 20
pulsen = 0
water_flow = 0

sw_level_max = 26


def flow_puls_callback(pin):
    global pulsen
    global water_flow
    pulsen += 1

    water_flow = pulsen * 2.25

    print(f"FLOW : {water_flow} ml")


def max_level_callback(pin):
    print("ALERT: Max level detected!")


def setup():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(flowsens, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(sw_level_max, GPIO.IN, GPIO.PUD_DOWN)

    GPIO.add_event_detect(flowsens, GPIO.RISING,
                          flow_puls_callback, bouncetime=20)

    GPIO.add_event_detect(sw_level_max, GPIO.FALLING,
                          max_level_callback, bouncetime=60)


setup()

try:
    while True:
        time.sleep(0.2)


except KeyboardInterrupt:
    print("programma gestopt")
finally:
    GPIO.cleanup()
