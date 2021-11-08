#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  show_servo_info.py - custom utility to show all the various servo data
#  based upon the code from York Hack Space May 2014
#  downloaded from https://github.com/RorschachUK/meArmPi

# the command path below assumes all the code is in a 'complete_projects' folder within the Maker Kit folder structure
# command to run: python3 /home/pi/RPi_maker_kit5/complete_projects/MeArm_v0-4/show_servo_info.py

import meArm     # import the custom meArm.py set of classes

def main():
    arm = meArm.meArm(debug=True)     # define the arm variable

    # the servo order from lowest channel number to highest must be:
    #  - base servo
    #  - left/elbow servo
    #  - right/shoulder
    #  - gripper
    # the four servos should use one of the 'blocks' 0-3 on the PCA9685 
    arm.begin(0,0x40)   # set all the initial servo variables when using channels 0, 1, 2 & 3 ie block 0
    #arm.begin(1,0x40)  # set all the initial servo variables when using channels 4, 5, 6 & 7 ie block 1
    #arm.begin(2,0x40)  # set all the initial servo variables when using channels 8, 9, 10 & 11 ie block 2
    #arm.begin(3,0x40)  # set all the initial servo variables when using channels 12, 13, 14 & 15 ie block 3

    arm.gotoPoint(0, 100, 50)
    xnow, ynow, znow = arm.getPos()
    print ("current x,y,z: " + str(xnow) + ", " + str(ynow) + ", " + str(znow) )

    arm.gotoPoint(0, 100, 50)
    xnow, ynow, znow = arm.getPos()
    print ("current x,y,z: " + str(xnow) + ", " + str(ynow) + ", " + str(znow) )


if __name__ == '__main__':
    main()
