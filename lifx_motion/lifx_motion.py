#!/usr/bin/python
# coding=utf-8

import sys, time #Allows for controlling system functions (interrupt) and sleep times.
import os
import RPi.GPIO as GPIO #Tells python to use GPIO libraries
from lifxlan import LifxLAN, Light #Make sure 'pip install lifxlan' was run to enable lifx controls
from signal import pause #Not sure if this is needed after testing, but I'm 15 beers in and don't feel like playing with it.
from datetime import datetime #Allows for time delays. There's probably a better way to do this but I don't know how to do it. 

#Instantiate lifxlan
lifxlan = LifxLAN()

#Setup for master light for power state polling
lightmac1="d0:73:d5:28:08:19"
lightIP1="192.168.5.69"

#Setup GPIO pins as BCM (Broadcom). Physical pin for PIR sensor input is 16.
GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.IN,GPIO.PUD_DOWN)

#Set the master light variables required for polling. Called as 'doorlight'.
doorlight = Light(lightmac1,lightIP1)
#Set the group of lights to control. Other option is to send to all lights, but this affects everyroom on the network.
officelights=lifxlan.get_devices_by_group("Office")

#This entire thing was hacked together. Ideally I would like it to not check for power so often as to minimize network traffic to the lights. I'm still thinking how to do this. Something maybe like 'Check for motion, if no motion then loop. If motion then turn lights on.' 
#But then how would the lights get turned off when there's no motion?
#Also, I'm not sure if the 'now' and 'dt_string' variables are needed every time before a print. I have a feeling that if they're not then it would read once globally and that would be the value. A possible option is to look into turning the date/time variables into a function and calling that everytime?
def Main():
	while True:
		i = GPIO.input(23)
		if i==0:                 #When output from motion sensor is LOW
			now = datetime.now()
                        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
			print dt_string, "No Motion Detected. Pin reads", i
			while True:
				try:
					powerstatus=Light.get_power(doorlight)
				except:
					now = datetime.now()
					dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
					print dt_string, "Couldn't get powerstatus while no motion is detected. Return is", powerstatus
					continue
				break
			now = datetime.now()
                        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
			print dt_string, "Before no motion power check", powerstatus
			if powerstatus != 0: #Check if lights are currently turned on
				now = datetime.now()
                                dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
				print dt_string, "After power check inside no motion", powerstatus
				officelights.set_power(0) #Turn lights off
			time.sleep(10)
		elif i==1:               #When output from motion sensor is HIGH
			now = datetime.now()
                        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
			print dt_string, "Motion Detected. Pin reads", i
			while True:
				try:
					powerstatus=Light.get_power(doorlight)
				except:
					now = datetime.now()
                                        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
					print dt_string, "Couldn't get powerstatus while motion is detected. Return is", powerstatus
					continue
				break
			now = datetime.now()
                        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
			print dt_string, "Motion detected powerstatus", powerstatus
			if powerstatus == 0: #Check if lights are currently turned off
				now = datetime.now()
                                dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
				print dt_string, "After power check inside motion detected", powerstatus
				officelights.set_power(65535) #Turn lights on full
			time.sleep(600)
#If this is installed as a service then I'm not entirely sure this is necessary. However, I need to look into any cleanup requirements (GPIO.cleanup) when failure occurs while running as a service.
if __name__ == '__main__':
    try:
        Main()
    except KeyboardInterrupt:
	now = datetime.now()
        dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
        print dt_string, "CTRL+C entered. Running cleanup!"
        try:
	    GPIO.cleanup()
            sys.exit(0)
        except SystemExit:
            os._exit(0)
