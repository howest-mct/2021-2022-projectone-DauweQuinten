import time
import serial
from RPi import GPIO
import threading

from flask_cors import CORS
from flask_socketio import SocketIO, emit, send
from flask import Flask, jsonify, request
from repositories.DataRepository import DataRepository

from selenium import webdriver
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options


# Code voor Hardware
ser = serial.Serial('/dev/ttyS0')

# Code voor Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'geheim!'
socketio = SocketIO(app, cors_allowed_origins="*", logger=False,
                    engineio_logger=False, ping_timeout=1)

CORS(app)


@socketio.on_error()        # Handles the default namespace
def error_handler(e):
    print(e)


# API ENDPOINTS
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


# sockets


@socketio.on('connect')
def initial_connection():
    print('A new client connect')


# threads

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
    prev_dist = 0
    sensitivity = 10

    while True:
        data = get_distance_data()
        if(data):
            dist = get_distance_value(data)
            socketio.emit("B2F_ultrasonic_data", {"value": dist})

            if not (prev_dist - sensitivity < dist < prev_dist + sensitivity):
                DataRepository.insert_historiek(dist, 1, "level measurement")
                prev_dist = dist


def start_main_thread():
    print("**** Starting main code ****")
    sensiThread = threading.Thread(
        target=start_main_loop, args=(), daemon=True)
    sensiThread.start()


# ANDRE FUNCTIES


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


if __name__ == '__main__':
    try:
        start_chrome_thread()
        start_main_thread()
        print("**** Starting APP ****")
        socketio.run(app, debug=False, host='0.0.0.0')

    except KeyboardInterrupt:
        print('KeyboardInterrupt exception is caught')
    finally:
        GPIO.cleanup()
