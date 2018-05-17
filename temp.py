# -*- coding: utf-8 -*-
"""Python script to read temperature.

I plug the sensor data into pin 4 on the raspberry pi which requires pin 4 to
be a gpio pin. If the modprobe commands don't results in the device showing up
in the bus folder then make sure the following line is in `/boot/config.txt`

```
dtoverlay=w1-gpio,gpiopin=4
```

After rebooting the files should show up.
"""
import glob
import os
import time

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


def read_temp_raw():
    """Read the raw temperature from the device."""
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    """Read the temperature of the probe."""
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


while True:
        print(read_temp())
        time.sleep(1)
