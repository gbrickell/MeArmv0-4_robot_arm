#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  Demo_x-axis.py - created in Sept 2018 and further updated for the Raspberry Pi Maker Kit in Nov'21 
#   move the gripper along the x-axis keeping y and z constant
#  based upon the original code from York Hack Space May 2014 that was
#   downloaded from https://github.com/RorschachUK/meArmPi


# the command path below assumes all the code is in a 'complete_projects' folder within the Maker Kit folder structure
# command to run in Terminal window:   python3 ./RPi_maker_kit5/complete_projects/MeArm_v0-4/Demo_x-axis.py
#  - assumes the code is in the /home/YOURUSERNAME/RPi_maker_kit5/complete_projects/MeArm_v0-4 folder
# or just use Thonny IDE

####################################################################
#  basic buzzer functions
####################################################################

def buzz(frequency, length, installed):	 #function "buzz" is fed the pitch (frequency) and duration (length in seconds)
    # allow for a 'silent' duration
    if(frequency==0):
        time.sleep(length)
        return
    period = 1.0 / frequency 		     #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
    delayValue = period / 2		         #calcuate the time for half of the wave
    numCycles = int(length * frequency)	 #the number of waves to produce is the duration times the frequency

    for i in range(numCycles):		   #start a loop from 0 to the variable "cycles" calculated above
        GPIO.output(buzzer_pin, True)  #set buzzer pin to high
        time.sleep(delayValue)		   #wait with buzzer pin high
        GPIO.output(buzzer_pin, False) #set buzzer pin to low
        time.sleep(delayValue)		   #wait with buzzer pin low

def beep(number, length):  # simple function for beep length and on/off for 'number' times at standard beep frequency 1200Hz
    for i in range(1, number+1):
        #print ("beep: " + str(i))
        buzz(1200, length, 'yes')
        time.sleep(length)

####################################################################
#  function to set a LED ON/OFF
#   - assumes the LED_pin is already set as an OUTPUT
####################################################################
def LED_set(LED_pin, set):
    if set == 'ON':
        GPIO.output(LED_pin, 1)
    else:
        GPIO.output(LED_pin, 0)

#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#
# main code 
#
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

import time      # import the time library
import meArm     # import the custom meArm.py set of classes
# arm starts at the standard home position of (0, 100, 50)

################################
# GPIO set up
################################
import RPi.GPIO as GPIO # Import the GPIO Library - still using this for PWM
# Set the GPIO modes using GPIO 
GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False) 

#################
# buzzer set up 
#################
buzzer_pin = 12
GPIO.setup(buzzer_pin, GPIO.OUT)

##################
# RGB LED set up 
###################
RGB_red = 22
RGB_green = 27
RGB_blue = 17
GPIO.setup(RGB_red, GPIO.OUT)
GPIO.setup(RGB_green, GPIO.OUT)
GPIO.setup(RGB_blue, GPIO.OUT)
LED_set(RGB_red, 'ON')
LED_set(RGB_green, 'OFF')
LED_set(RGB_blue, 'OFF')

def main():
    arm = meArm.meArm(debug=False)     # define the arm variable
    # the servo order from lowest channel number to highest must be:
    #  - base servo
    #  - left/elbow servo
    #  - right/shoulder
    #  - gripper
    # the four servos should use one of the 'blocks' 0-3 on the PCA9685 
    #arm.begin(0,0x40)   # set all the initial servo variables when using channels 0, 1, 2 & 3 ie block 0
    #arm.begin(1,0x40)  # set all the initial servo variables when using channels 4, 5, 6 & 7 ie block 1
    #arm.begin(2,0x40)  # set all the initial servo variables when using channels 8, 9, 10 & 11 ie block 2
    arm.begin(3,0x40)  # set all the initial servo variables when using channels 12, 13, 14 & 15 ie block 3

    print ("set point 0")
    arm.gotoPoint(-100, 100, 50)   # keep y and z positions constant
    xnow, ynow, znow = arm.getPos()
    print ("current x,y,z: " + str(xnow) + ", " + str(ynow) + ", " + str(znow) )
    beep(2, 0.1)  # 0.1 second beep x2 
    LED_set(RGB_red, 'OFF')
    LED_set(RGB_green, 'ON')
    time.sleep(2)   # short pause
    LED_set(RGB_red, 'ON')
    LED_set(RGB_green, 'OFF')

    print ("set point 1")
    arm.gotoPoint(-50, 100, 50)     # keep y and z positions constant
    xnow, ynow, znow = arm.getPos()
    print ("current x,y,z: " + str(xnow) + ", " + str(ynow) + ", " + str(znow) )
    beep(2, 0.1)  # 0.1 second beep x2 
    LED_set(RGB_red, 'OFF')
    LED_set(RGB_green, 'ON')
    time.sleep(2)   # short pause
    LED_set(RGB_red, 'ON')
    LED_set(RGB_green, 'OFF')

    print ("set point 2")
    arm.gotoPoint(0, 100, 50)   # keep y and z positions constant
    xnow, ynow, znow = arm.getPos()
    print ("current x,y,z: " + str(xnow) + ", " + str(ynow) + ", " + str(znow) )
    beep(2, 0.1)  # 0.1 second beep x2 
    LED_set(RGB_red, 'OFF')
    LED_set(RGB_green, 'ON')
    time.sleep(2)   # short pause
    LED_set(RGB_red, 'ON')
    LED_set(RGB_green, 'OFF')

    print ("set point 3")
    arm.gotoPoint(50, 100, 50)   # keep y and z positions constant
    xnow, ynow, znow = arm.getPos()
    print ("current x,y,z: " + str(xnow) + ", " + str(ynow) + ", " + str(znow) )
    beep(2, 0.1)  # 0.1 second beep x2 
    LED_set(RGB_red, 'OFF')
    LED_set(RGB_green, 'ON')
    time.sleep(2)   # short pause
    LED_set(RGB_red, 'ON')
    LED_set(RGB_green, 'OFF')

    print ("set point 4")
    arm.gotoPoint(100, 100, 50)   # keep y and z positions constant
    xnow, ynow, znow = arm.getPos()
    print ("current x,y,z: " + str(xnow) + ", " + str(ynow) + ", " + str(znow) )
    beep(2, 0.1)  # 0.1 second beep x2 
    LED_set(RGB_red, 'OFF')
    LED_set(RGB_green, 'ON')
    time.sleep(2)   # short pause
    LED_set(RGB_red, 'ON')
    LED_set(RGB_green, 'OFF')

    print ("set point 5")
    arm.gotoPoint(0, 100, 50)   # back to home position to finish
    xnow, ynow, znow = arm.getPos()
    print ("current x,y,z: " + str(xnow) + ", " + str(ynow) + ", " + str(znow) )
    beep(2, 0.1)  # 0.1 second beep x2 
    LED_set(RGB_red, 'OFF')
    LED_set(RGB_green, 'ON')
    time.sleep(2)   # short pause
    LED_set(RGB_green, 'OFF')

if __name__ == '__main__':
    main()
