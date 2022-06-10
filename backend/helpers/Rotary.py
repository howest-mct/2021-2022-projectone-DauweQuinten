from RPi import GPIO

# !!! Important note !!! : Delay in main-loop is noodzakeling om een correcte werking te verkrijgen


class Rotary:

    def __init__(self, clk, dt, sw) -> None:
        self.__clk = clk
        self.__dt = dt
        self.__sw = sw
        self.__clkLastState = False
        self.counter = 0
        self.__setup_encoder()

    def __setup_encoder(self):
        print("SETUP...")
        GPIO.setmode(GPIO.BCM)

        GPIO.setup(self.__sw, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__clk, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.__dt, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.__sw, GPIO.FALLING,
                              self.__encoder_click_callback, bouncetime=200)

        GPIO.add_event_detect(self.__clk, GPIO.BOTH,
                              self.__rotation_decode, bouncetime=1)

        print("Setup done!")

    def __encoder_click_callback(self, pin):
        print('click')

    def __rotation_decode(self, pin):
        clk = GPIO.input(self.__clk)
        dt = GPIO.input(self.__dt)
        if clk != self.__clkLastState and clk and not dt:
            self.counter += 1
        elif clk != self.__clkLastState and clk and dt:
            self.counter -= 1

    def cleanup(self):
        print("Cleaning up some GPIO...")
        GPIO.cleanup()
        print("Cleanup done!")

    def switch_is_pressed(self):
        if not GPIO.input(self.__sw):
            return True
        else:
            return False


# region **** Mogelijke aanvullingen ****

# setCounterBoundaries(min, max) -> Stelt een min- en max-waarde in voor de counter


# endregion
