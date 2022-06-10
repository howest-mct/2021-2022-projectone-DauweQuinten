from RPi import GPIO
import time
from smbus import SMBus


class i2c_LCD:

    def __init__(self, slave_addr, rs, klok) -> None:
        self.__slave = slave_addr
        self.__rs = rs
        self.__klok = klok
        self.__i2c = SMBus()
        self.__i2c.open(1)

    def __set_data_bits(self, byte):
        self.__i2c.write_byte(self.__slave, byte)

    def init_LCD(self):
        # Display set
        self.send_instruction(14 << 2)
        # Display on
        self.send_instruction(15)
        # clear display & cursor home
        self.send_instruction(1)

    def send_instruction(self, value):
        GPIO.output(self.__rs, 0)
        GPIO.output(self.__klok, 1)
        self.__set_data_bits(value)
        GPIO.output(self.__klok, 0)
        time.sleep(0.01)

    def send_character(self, value):
        GPIO.output(self.__rs, 1)
        GPIO.output(self.__klok, 1)
        self.__set_data_bits(value)
        GPIO.output(self.__klok, 0)
        time.sleep(0.01)

    def write_message(self, message, auto_enter=False, auto_shift=False):
        if len(message) <= 32:
            for i in range(len(message)):
                if i == 16 and auto_enter:
                    self.move_cursor(0x40)
                self.send_character(ord(message[i]))
        else:
            for i in range(len(message)):
                self.send_character(ord(message[i]))
            if auto_shift:
                for i in range(80):
                    self.shift_canvas_left()

    def clear_display(self):
        self.send_instruction(1)

    def shutdown(self):
        self.send_instruction(8)
        self.__i2c.close()

    def move_cursor(self, adres):
        self.send_instruction(128 | adres)

    def enter(self):
        self.move_cursor(0x40)

    # stel de cursor modus in
    def set_cursor(self, mode):

        if type(mode) is int:
            # mode 0: Cursor off
            if mode == 0:
                self.send_instruction(12)

            # mode 1: Cursor on
            elif mode == 1:
                self.send_instruction(14)

            # mode 3: Cursor blink
            elif mode == 2:
                self.send_instruction(15)
            else:
                print("Ongeldige cursormode!")
        else:
            print("FOUT: Cursormode moet een integer zijn!")

    def shift_canvas_left(self, delay=0.3):
        self.send_instruction(0x18)
        time.sleep(delay)

    def shift_canvas_right(self, delay=0.3):
        self.send_instruction(0x1C)
        time.sleep(delay)

    def create_custom_char(self, adres, list_bitmap):
        self.send_instruction(0x40 | adres << 3)
        for bits in list_bitmap:
            self.send_character(bits)
