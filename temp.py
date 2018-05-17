#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Python script to read temperature from DS18B20.

I plug the sensor data into pin 4 on the raspberry pi which requires pin 4 to
be a gpio pin. If the modprobe commands don't results in the device showing up
in the bus folder then make sure the following line is in `/boot/config.txt`:

```
dtoverlay=w1-gpio,gpiopin=4
```

After rebooting and the script should work.
"""
import glob
import os
import time

def enable_kernel_modules():
    """Enable kernel modules."""
    os.system('modprobe w1-gpio')
    os.system('modprobe w1-therm')

def get_device_file():
    """Get the path to the the data file."""
    base_dir = '/sys/bus/w1/devices/'
    device_folder = glob.glob(base_dir + '28*')[0]
    device_file = device_folder + '/w1_slave'
    return device_file


def read_device_file(device_file):
    """Read the raw temperature from the device."""
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def parse_raw_input(raw_input):
    """Parse raw data into temperatures."""
    # Error reading, return nothing
    if raw_input[0].strip()[-3:] != 'YES':
        return None, None
    equals_pos = raw_input[1].find('t=')
    if equals_pos != -1:
        temp_string = raw_input[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return temp_c, temp_f
    else:
        return None, None

def main():
    """Main Function."""
    enable_kernel_modules()
    device_file = get_device_file()
    while True:
        raw_input = read_device_file(device_file)
        print(parse_raw_input(raw_input))


if __name__ == '__main__':
    """Run main routine."""
    main()
