from multiprocessing import Process
import csv
import gpsd
import glob
from smbus2 import SMBus
import time

def gps():
    # setup csv file
    file = "gps_log.csv"
    fields = ['time', 'lon', 'lat', 'speed']
    countdown = 1800 * 2 # countdown is how many seconds we will gather data for

    # connect to GPS module
    gpsd.connect()

    with open(file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(fields)
        count = 0
        
        while count < countdown:
            now = time.localtime()
            current_time = time.strftime("%H:%M:%S", now)
            packet = gpsd.get_current()
            csvwriter.writerow([current_time, "{:.4f}".format(packet.lon), "{:.4f}".format(packet.lat), "{:.4f}".format(packet.hspeed)])
            count = count +1
            time.sleep(0.5) # frequency of data acquisition is .5 second
            
def read_temp_raw():
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f

def ds18b20():
    # setup csv file
    file = "ds18b20_log.csv" 
    fields = ['time', 'temperature']
    countdown = 1800 * 1
        
    with open(file, 'w') as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=',')
        csvwriter.writerow(fields)
        count = 0
        while count < countdown:
            now = time.localtime()
            current_time = time.strftime("%H:%M:%S", now)
            temp_c, temp_f = read_temp()
            csvwriter.writerow([current_time, "{:.4f}".format(temp_c)])
            count = count + 1
            time.sleep(.2)
    
def si7021():
    # setup csv file
    file = "si7021_log.csv"
    fields = ['time', 'humidity', 'temperature']
    countdown = 1800 * 10

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
            time.sleep(.082)

def main():
    p1 = Process(target=gps)
    p2 = Process(target=ds18b20)
    p3 = Process(target=si7021)
    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()
    print("Finished")

if __name__ == '__main__':
    main()

