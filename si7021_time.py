from smbus2 import SMBus
from timeit import default_timer as timer
import time

# setup bus connection
bus = SMBus(1)

count = 0
avg = 0

while count < 100:
    start = timer()
    bus.write_byte(0x40, 0xE5)
    data0 = bus.read_byte(0x40, 0x40)
    data1 = bus.read_byte(0x40, 0x40)
    humidity = ((data0 * 256 + data1) * 125 / 65536.0) - 6
    bus.write_byte(0x40, 0xE0)
    data0 = bus.read_byte(0x40, 0x40)
    data1 = bus.read_byte(0x40, 0x40)
    tempc = ((data0 * 256 + data1) * 175.72 / 65536.0) - 46.85
    time.sleep(.082)
    end = timer()
    avg = avg + (end - start)
    count = count + 1
    
print("Average Sensor Access Time (in seconds) over 100 readings:", avg/100)