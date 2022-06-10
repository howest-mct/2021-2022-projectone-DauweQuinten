import time
import serial
from RPi import GPIO

from helpers.i2c_LCD import i2c_LCD
from helpers.Rotary import Rotary

import threading
import subprocess
from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request
from repositories.DataRepository import DataRepository

from selenium import webdriver
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options


# region global code voor Hardware
ser = serial.Serial('/dev/ttyS0')

# lcd
rs_pin = 24
E_pin = 23
lcd = i2c_LCD(0x20, rs_pin, E_pin)


# rotary encoder
rotary = Rotary(6, 22, 27)


# GPIO flowsensor
flowsens = 20
pulsen = 0
water_flow = 0

# GPIO max level switch
sw_level_max = 26
emergency_stop = False


# GPIO ventiel
ventiel = 21
valve_state = 0


# endregion

# region Code voor Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)

# endregion

# region API ENDPOINTS
endpoint = '/api/v1'


@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."


@app.route(endpoint + '/devices/', methods=['GET'])
def get_devices():
    data = DataRepository.read_devices()
    return jsonify(data), 200


@app.route(endpoint + '/devices/<deviceid>/', methods=['GET'])
def get_device(deviceid):
    data = DataRepository.read_device(deviceid)
    return jsonify(data), 200


@app.route(endpoint + '/historiek/', methods=['GET', 'POST'])
def get_historiek():
    if request.method == "GET":
        data = DataRepository.read_historiek()
        return jsonify(data), 200
    elif request.method == 'POST':
        try:
            data = DataRepository.json_or_formdata(request)
            value = data['value']
            deviceid = data['deviceid']
            commentaar = data['commentaar']

            result = DataRepository.insert_historiek(
                value, deviceid, commentaar)
            if result > 0:
                return jsonify(status='OK'), 204
            elif result == 0:
                return jsonify(status='error'), 404
        except Exception:
            return jsonify(status='error'), 400

# endregion


# region sockets

@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)


@socketio.on('connect')
def initial_connection():
    print('A new client connect')
    response = DataRepository.read_device_state(4)
    print(response)
    emit('B2F_initial-valve-state', {'state': response['status']})


@socketio.on('F2B_switch_valve')
def switch_valve(payload):
    global valve_state
    print(payload)
    state = payload['state']
    DataRepository.insert_historiek(state, 4, 2, "manueel bediend")
    DataRepository.update_device_state(4, state)

    response = DataRepository.read_device_state(4)
    new_state = response['status']
    emit("B2F_switched_valve", {'state': new_state})

    valve_state = new_state

    if state == 0:
        DataRepository.insert_historiek(
            water_flow, 3, 1, "Hoeveelheid water bijgevuld")


# endregion

# region threads


def start_chrome_kiosk():
    import os

    os.environ['DISPLAY'] = ':0.0'
    options = webdriver.ChromeOptions()
    # options.headless = True
    # options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36")
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--allow-running-insecure-content')
    options.add_argument("--disable-extensions")
    # options.add_argument("--proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--start-maximized")
    options.add_argument('--disable-gpu')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--kiosk')
    # chrome_options.add_argument('--no-sandbox')
    # options.add_argument("disable-infobars")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)

    driver = webdriver.Chrome(options=options)
    driver.get("http://localhost")


def start_chrome_thread():
    print("**** Starting CHROME ****")
    chromeThread = threading.Thread(
        target=start_chrome_kiosk, args=(), daemon=True)
    chromeThread.start()


def start_main_loop():

    global water_flow
    global valve_state
    prev_dist = 0
    sensitivity = 10

    prev_valve_state = 0

    # region configuratie

    min_level = 500
    max_level = 100

    # endregion

    while True:
        data = get_distance_data()
        if(data):
            dist = get_distance_value(data)
            socketio.emit("B2F_ultrasonic_data", {"value": dist})

            if not (prev_dist - sensitivity < dist < prev_dist + sensitivity):
                DataRepository.insert_historiek(
                    dist, 1, 1, "level measurement")
                prev_dist = dist

        if dist > min_level and not emergency_stop:
            valve_state = 1
            if valve_state != prev_valve_state:
                DataRepository.insert_historiek(1, 4, 2, "vullen gestart")
                prev_valve_state = valve_state

        if (dist < max_level) or emergency_stop:
            valve_state = 0
            if valve_state != prev_valve_state:
                DataRepository.insert_historiek(0, 4, 2, "vullen gestopt")
                DataRepository.insert_historiek(
                    water_flow, 3, 1, "Hoeveelheid water bijgevuld")
                water_flow = 0
                prev_valve_state = valve_state
                DataRepository.update_device_state(4, valve_state)

        GPIO.output(ventiel, valve_state)
        DataRepository.update_device_state(4, valve_state)
        socketio.emit("B2F_changed_by_hardware", {'state': valve_state})


def start_main_thread():
    print("**** Starting main code ****")
    sensiThread = threading.Thread(
        target=start_main_loop, args=(), daemon=True)
    sensiThread.start()


def start_lcd():

    prev_lcd_state = 0

    rotary.counter = 1
    prev_counter = 0
    min_counter = 1
    max_counter = 2

    while True:

        if rotary.counter != prev_counter:

            if rotary.counter > max_counter:
                rotary.counter = min_counter
            elif rotary.counter < min_counter:
                rotary.counter = max_counter

            print(rotary.counter)
            prev_counter = rotary.counter

        # lcd states
        if rotary.counter == 1:
            if rotary.counter != prev_lcd_state:
                prev_lcd_state = rotary.counter
                schrijf_ip_naar_display()
            else:
                lcd.shift_canvas_left()

        elif rotary.counter == 2:
            if rotary.counter != prev_lcd_state:
                prev_lcd_state = rotary.counter
                show_screen_2()


def start_lcd_thread():
    print("**** Starting lcd code ****")
    lcdThread = threading.Thread(
        target=start_lcd, args=(), daemon=True)
    lcdThread.start()


# endregion

# region ANDERE FUNCTIES


def setup():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(flowsens, GPIO.IN, GPIO.PUD_DOWN)
    GPIO.setup(sw_level_max, GPIO.IN, GPIO.PUD_DOWN)

    GPIO.add_event_detect(flowsens, GPIO.RISING,
                          flow_puls_callback, bouncetime=20)

    GPIO.add_event_detect(sw_level_max, GPIO.FALLING,
                          max_level_callback, bouncetime=60)

    GPIO.setup(ventiel, GPIO.OUT)

    GPIO.setup(rs_pin, GPIO.OUT)
    GPIO.setup(E_pin, GPIO.OUT)

    lcd.init_LCD()
    lcd.set_cursor(0)
    lcd.write_message("Hello World!")
    lcd.enter()
    lcd.write_message("starting up...")
    time.sleep(2)


def get_distance_data():
    data_bytes = []
    data = ser.read()
    int_data = int.from_bytes(data, "big")

    if int_data == 0xff:
        data_bytes.append(int_data)

        for i in range(3):
            int_data = int.from_bytes(ser.read(), "big")
            data_bytes.append(int_data)
        return data_bytes


def get_distance_value(data):
    data_h = data[1]
    data_l = data[2]
    return (data_h << 8) | data_l


# Get ip-address uit een file en return hem in een string
def get_ip_string(interface):
    ip_file = str(subprocess.check_output(['ifconfig', interface]))
    ip_start_index = ip_file.find("inet ") + 5
    ip_end_index = ip_file.find(" netmask")
    ip = ip_file[ip_start_index: ip_end_index]
    return f"{interface}: {ip}"


# display state 1: Schrijf ip-adressen naar de display
def schrijf_ip_naar_display():
    lcd.clear_display()
    wlan0 = get_ip_string('wlan0')
    lcd.write_message(wlan0)


# display state 2: show current water volume
def show_screen_2():
    lcd.clear_display()
    lcd.write_message("Scherm 2")

# endregion

# region CALLBACKS


def flow_puls_callback(pin):
    global pulsen
    global water_flow
    pulsen += 1

    water_flow = pulsen * 2.25

    print(f"FLOW : {water_flow} ml")


def max_level_callback(pin):

    global emergency_stop
    print("ALERT: Max level detected!")
    emergency_stop = True
    DataRepository.insert_historiek(1, 2, 1, "Max level detected")
    DataRepository.update_device_state(2, 1)


# endregion


# region MAIN
if __name__ == '__main__':
    try:
        setup()
        # start_chrome_thread()
        start_main_thread()
        start_lcd_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')

    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        GPIO.output(ventiel, 0)
        lcd.shutdown()
        GPIO.cleanup()

# endregion
