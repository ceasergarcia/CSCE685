import gpsd
import time
from timeit import default_timer as timer

# connect to GPS module
gpsd.connect()

count = 0
avg = 0
while count < 100:
    start = timer()
    packet = gpsd.get_current()
    lon = packet.lon
    lat = packet.lat
    time.sleep(0.5)
    end = timer()
    avg = avg + (end - start)
    count = count + 1
    
print("Average Sensor Access Time (in seconds) over 100 readings:", avg/100)