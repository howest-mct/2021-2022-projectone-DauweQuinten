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
is_shutdowned = False

# lcd
rs_pin = 24
E_pin = 23
lcd_state = 1
lcd = i2c_LCD(0x20, rs_pin, E_pin)


# rotary encoder
rotary = Rotary(6, 22, 27)

# volume variabelen
current_volume = 0
prev_volume = 0
min_volume = 0
max_volume = 0

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


@app.route(endpoint + '/configuration/', methods=['GET', 'PUT'])
def get_configuration():
    if request.method == 'GET':
        data = DataRepository.read_configuration()
        return jsonify(data), 200
    elif request.method == 'PUT':
        gegevens = DataRepository.json_or_formdata(request)
        print(gegevens)
        for setting in gegevens.items():
            setting_data = setting[1][0]
            config_id = setting_data['id']
            new_value = setting_data['value']
            result = DataRepository.update_configuration(config_id, new_value)
            if result < 0:
                return jsonify(state='error'), 400
            print(setting)

        return jsonify(state='OK'), 200


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

    response = DataRepository.read_device_state(2)
    print(response)
    emit('B2F_initial-switch-state', {'state': response['status']})
    global emergency_stop
    emergency_stop = response['status']


@socketio.on('F2B_switch_valve')
def switch_valve(payload):
    global valve_state
    print(payload)
    state = payload['state']
    DataRepository.insert_historiek(state, 4, 2, "manueel bediend")
    DataRepository.update_device_state(4, state)

    response = DataRepository.read_device_state(4)
    new_state = response['status']
    socketio.emit("B2F_switched_valve", {'state': new_state})
    valve_state = new_state

    if state == 0:
        DataRepository.insert_historiek(
            water_flow, 3, 1, "Hoeveelheid water bijgevuld")


@socketio.on('F2B_shutdown')
def shutdown(payload):
    print(payload)
    global is_shutdowned
    is_shutdowned = True
    shutdown_raspberry_pi()


@socketio.on('F2B_submit_times')
def get_volume_between(payload):
    print(payload)
    start = payload['start']
    end = payload['end']
    response = DataRepository.read_historiek_between(1, start, end)
    for record in response:
        record['waarde'] = round(calc_current_volume(record['waarde']), 2)
        print(record)
    emit("B2F_historiek_data", {"data": response})


@socketio.on('F2B_update_config')
def set_new_config(payload):
    global min_volume
    global max_volume
    config = get_current_config()
    min_volume = config['min']
    max_volume = config['max']

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
    global pulsen
    global valve_state
    global current_volume
    global min_volume
    global max_volume
    prev_dist = 0
    sensitivity = 10
    prev_valve_state = 0

    # region configuratie

    config = get_current_config()
    min_volume = config['min']
    max_volume = config['max']

    # endregion

    while True:
        data = get_distance_data()
        if(data):
            dist = get_distance_value(data)
            current_volume = calc_current_volume(dist)
            socketio.emit("B2F_current_volume", {"value": current_volume})

            if not (prev_dist - sensitivity < dist < prev_dist + sensitivity):
                DataRepository.insert_historiek(
                    dist, 1, 1, "level measurement")
                prev_dist = dist

        if (current_volume < min_volume) and not emergency_stop:
            valve_state = 1
            if valve_state != prev_valve_state:
                DataRepository.insert_historiek(1, 4, 2, "vullen gestart")
                prev_valve_state = valve_state

        if (current_volume > max_volume) or emergency_stop:
            valve_state = 0
            if valve_state != prev_valve_state:
                DataRepository.insert_historiek(0, 4, 2, "vullen gestopt")
                DataRepository.insert_historiek(
                    water_flow, 3, 1, "Hoeveelheid water bijgevuld")
                prev_valve_state = valve_state
                DataRepository.update_device_state(4, valve_state)
                water_flow = 0
                pulsen = 0

        GPIO.output(ventiel, valve_state)
        DataRepository.update_device_state(4, valve_state)
        socketio.emit("B2F_changed_by_hardware", {'state': valve_state})


def start_main_thread():
    print("**** Starting main code ****")
    sensiThread = threading.Thread(
        target=start_main_loop, args=(), daemon=True)
    sensiThread.start()


def start_lcd():

    global current_volume
    global is_shutdowned
    global lcd_state
    global emergency_stop

    prev_lcd_state = 0
    rotary.counter = 1
    prev_counter = 0
    min_counter = 1
    max_counter = 3

    while True:

        # hold counter into range
        if rotary.counter != prev_counter:

            if rotary.counter > max_counter:
                rotary.counter = min_counter
            elif rotary.counter < min_counter:
                rotary.counter = max_counter

            print(rotary.counter)
            prev_counter = rotary.counter

        # lcd states
        if(not emergency_stop):
            lcd_state = rotary.counter

        print(lcd_state)

        if (lcd_state == 2) and (is_shutdowned == False):
            if lcd_state != prev_lcd_state:
                schrijf_ip_naar_display()
                prev_lcd_state = lcd_state
            else:
                lcd.shift_canvas_left()

        elif lcd_state == 1:

            if lcd_state != prev_lcd_state:
                lcd.clear_display()
                lcd.write_message("Volume (liter):")
                lcd.enter()
                lcd.write_message(f"{str(round(current_volume, 1))}")
                prev_lcd_state = lcd_state
            else:
                show_current_volume()

        elif lcd_state == 3:
            if lcd_state != prev_lcd_state:
                lcd.clear_display()
                lcd.write_message("Uitschakelen ?")
                prev_lcd_state = lcd_state

            if rotary.switch_is_pressed():
                is_shutdowned = True
                shutdown_raspberry_pi()
        elif lcd_state == 4:
            if lcd_state != prev_lcd_state:
                lcd.clear_display()
                lcd.write_message("Vergrendeld... druk om te ontgrendelen")
                prev_lcd_state = lcd_state
            else:
                lcd.shift_canvas_left()
                if rotary.switch_is_pressed():
                    emergency_stop = 0
                    lcd_state = 1
                    rotary.counter = 1
                    DataRepository.insert_historiek(
                        0, 2, 1, "noodstop ontgrendeld")
                    DataRepository.update_device_state(2, 0)
                    socketio.emit("B2F_unlock_emergency_stop",
                                  {"status": "unlocked"})


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

    set_emergency_stop()

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


def calc_current_volume(distance):
    # dimensions in mm
    area = 32300
    height = 180

    # calculation
    water_level = height - distance
    water_volume = (water_level * area)/1000000
    return water_volume


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
def show_current_volume():
    global current_volume
    global prev_volume

    if not (prev_volume - 0.2) < current_volume < (prev_volume + 0.2):
        lcd.enter()
        lcd.write_message(f"{str(round(current_volume, 1))}")
        prev_volume = current_volume


def shutdown_raspberry_pi():
    print('uitschakelen...')
    lcd.clear_display()
    lcd.write_message('uitschakelen...')
    lcd.enter()
    lcd.write_message('Bye!')
    time.sleep(2)
    GPIO.output(ventiel, 0)
    lcd.clear_display()
    ser.close()
    lcd.shutdown()
    GPIO.cleanup()
    subprocess.Popen(['sudo', 'shutdown', '-h', 'now'])
    exit(0)


def get_current_config():

    config_data = DataRepository.read_configuration()
    min_volume = float(config_data[0]['value'])
    fill_amount = float(config_data[1]['value'])
    max_volume = min_volume + fill_amount

    return {'min': min_volume, 'max': max_volume}


def set_emergency_stop():
    response = DataRepository.read_device_state(2)
    print(response)
    global emergency_stop
    global lcd_state
    emergency_stop = response['status']
    if(emergency_stop == 1):
        lcd_state = 4


# endregion

# region CALLBACKS


def flow_puls_callback(pin):
    global pulsen
    global water_flow
    pulsen += 1

    water_flow = pulsen * 2.25


def max_level_callback(pin):
    global emergency_stop
    global lcd_state
    print("ALERT: Max level detected!")
    emergency_stop = True
    DataRepository.insert_historiek(1, 2, 1, "Max level detected")
    DataRepository.update_device_state(2, 1)
    socketio.emit('B2F_max_level_detected', {"status": "gestopt"})
    lcd_state = 4


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
        ser.close()
        GPIO.cleanup()

# endregion
