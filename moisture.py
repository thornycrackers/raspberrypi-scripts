#!/usr/bin/python3

import time

import RPi.GPIO as GPIO

moisture_pin = 21

GPIO.setmode(GPIO.BCM)
GPIO.setup(moisture_pin, GPIO.IN)

while True:
        print(GPIO.input(moisture_pin))
            time.sleep(1)

