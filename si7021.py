import csv
from smbus2 import SMBus
import time

# setup csv file
file = "si7021_log.csv"
fields = ['time', 'humidity', 'temperature']
countdown = 1 * 10

# setup bus connection
bus = SMBus(1)

with open(file, 'w') as csvfile:
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow(fields)
    count = 0
    
    while count < countdown:
        now = time.localtime()
        current_time = time.strftime("%H:%M:%S", now)
        bus.write_byte(0x40, 0xE5)
        data0 = bus.read_byte(0x40, 0x40)
        data1 = bus.read_byte(0x40, 0x40)
        humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
        bus.write_byte(0x40, 0xE0)
        data0 = bus.read_byte(0x40, 0x40)
        data1 = bus.read_byte(0x40, 0x40)
        tempc = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
        csvwriter.writerow([current_time, "{:.4f}".format(humidity), "{:.4f}".format(tempc)])
        count = count + 1
        time.sleep(0.1); # frequency of data acquisition is 0.1 seconds (100 milliseconds)
