import serial


ser = serial.Serial('/dev/ttyS0')

print(ser.name)


def get_distance_value(data):
    data_h = data[1]
    data_l = data[2]
    return (data_h << 8) | data_l


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


try:
    while True:

        dist_data = get_distance_data()
        dist = get_distance_value(dist_data)
        print(f"{dist} mm")


except KeyboardInterrupt:
    print("programma gestopt")
