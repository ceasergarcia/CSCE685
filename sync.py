import csv

# start with file that had lowest frequency
timestamps = []
with open("ds18b20_log.csv", newline='') as file_read:
    reader = csv.reader(file_read)
    next(reader) # skip header row

    # start reading rows to save timestamps into an array
    for row in reader:
        timestamps.append(row[0])

# downsample gps readings
with open("gps_sync.csv", 'w') as file_write:
    writer = csv.writer(file_write, delimiter=',')
    writer.writerow(['time', 'lon', 'lat', 'speed'])
    with open("gps_log.csv", newline='') as file_read:
        reader = csv.reader(file_read)
        next(reader) # skip header row

        index = 0
        # start reading rows
        for row in reader:
            # check if the current timestamp matches the timestamp of the base file
            if (index < len(timestamps) and row[0] == timestamps[index]):
                writer.writerow(row)
                index = index + 1

# downsample si7021 readings
with open("si7021_sync.csv", 'w') as file_write:
    writer = csv.writer(file_write, delimiter=',')
    writer.writerow(['time', 'humidity', 'temperature'])
    with open("si7021_log.csv", newline='') as file_read:
        reader = csv.reader(file_read)
        next(reader) # skip header row

        index = 0
        # start reading rows
        for row in reader:
            # check if the current timestamp matches the timestap of the base file
            if (index < len(timestamps) and row[0] == timestamps[index]):
                writer.writerow(row)
                index = index + 1