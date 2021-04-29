import csv
import gpsd
import time

# setup csv file
file = "gps_log.csv"
fields = ['time', 'lon', 'lat']
countdown = 1 * 60 # countdown is how many seconds we will gather data for

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
        csvwriter.writerow([current_time, "{:.4f}".format(packet.lon), "{:.4f}".format(packet.lat)])
        count = count +1
        time.sleep(1) # frequency of data acquisition is 1 second