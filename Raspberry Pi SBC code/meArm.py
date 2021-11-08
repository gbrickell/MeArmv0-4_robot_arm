# meArm.py - updates in July 2018 
#   to use python 3
#   to add some debug output
#   to add more annotation
#  further updates for use with the Raspberry Pi Maker Kit in Nov'21
#  based upon the code from York Hack Space May 2014
#  original code downloaded from https://github.com/RorschachUK/meArmPi

# A motion control library for the Phenoptix meArm:
#  - v0.4 laser cut acrylic version at https://www.thingiverse.com/thing:360108
#  - v0.4 3D printed version at https://www.thingiverse.com/thing:616239
#  - v0.4 updated/corrected 3D print designs for Raspberry Pi Maker Kit usage at Prusa web site 

# at some point the 'driver' used below and included with the original s/w set should be
#   substituted by the general purpose PCA9685 library

# this file should be in the same folder as the test code

from PCA9685_PWM_Servo_Driver import PWM
import kinematics     # this imports the custom code that does the polar/cartesian coordinate transformations
import time           # this imports the library that allows various time functions
from math import pi   # this allows the use of pi, calculated to reasonable precision, as a variable

# set the default 'sweep' values for each of the servos
# these should be adjusted/tweaked forthe set of servos that are being used
MinBase = 155       # usually 145
MaxBase = 49        # usually 49

MinShoulder = 118   # usually 118
MaxShoulder = 22    # usually 22

MinElbow = 144      # usually 144
MaxElbow = 36       # usually 36

MinGripper = 65     # usually 75
MaxGripper = 118    # usually 115


class meArm():        # class for all the various set up and usage functions for the robot arm

    def __init__(self, sweepMinBase = MinBase, sweepMaxBase = MaxBase, angleMinBase = -pi/4, angleMaxBase = pi/4, sweepMinShoulder = MinShoulder, sweepMaxShoulder = MaxShoulder, angleMinShoulder = pi/4, angleMaxShoulder = 3*pi/4, sweepMinElbow = MinElbow, sweepMaxElbow = MaxElbow, angleMinElbow = pi/4, angleMaxElbow = -pi/4, sweepMinGripper = MinGripper, sweepMaxGripper = MaxGripper, angleMinGripper = pi/2, angleMaxGripper = 0, debug=False):

        """Constructor for meArm - can use as default arm=meArm(), or supply calibration data for servos."""

        self.debug = debug

        self.servoInfo = {}
        if self.debug:
            print ("base info:")
        self.servoInfo["base"] = self.setupServo(sweepMinBase, sweepMaxBase, angleMinBase, angleMaxBase)
        if self.debug:
            print ("shoulder info:")
        self.servoInfo["shoulder"] = self.setupServo(sweepMinShoulder, sweepMaxShoulder, angleMinShoulder, angleMaxShoulder)
        if self.debug:
            print ("elbow info:")
        self.servoInfo["elbow"] = self.setupServo(sweepMinElbow, sweepMaxElbow, angleMinElbow, angleMaxElbow)
        if self.debug:
            print ("gripper info:")
        self.servoInfo["gripper"] = self.setupServo(sweepMinGripper, sweepMaxGripper, angleMinGripper, angleMaxGripper)

    	
    # The PCA9685 servo board has four 'blocks' of four servo connectors, referenced as
    #  0, 1, 2 or 3 and a unique I2C address which is unlikely to anything other than 0x40
    # If (say) you connect the servos to channels 12, 13, 14 & 15 then the 'block' ref is set to 3


    def begin(self, block = 0, address = 0x40):

        """Call begin() before any other meArm calls.  It has optional parameters to select a different block of servo connectors or a different I2C address."""

        if self.debug:
            print ("block: " + str(block) + " - address: " + str(address))
        self.pwm = PWM(address)         # Address of PCA9685 PWM servo I2C module
        self.base = block * 4           # channel for the **base** servo eg 12 if block 3
        if self.debug:
            print ("base servo channel set to " + str(self.base))
        self.shoulder = block * 4 + 1   # channel for the **shoulder** servo eg 13 if block 3
        if self.debug:
            print ("shoulder servo channel set to " + str(self.shoulder))
        self.elbow = block * 4 + 2      # channel for the **elbow** servo eg 14 if block 3
        if self.debug:
            print ("elbow servo channel set to " + str(self.elbow))
        self.gripper = block * 4 + 3    # channel for the **gripper** servo eg 15 if block 3
        if self.debug:
            print ("gripper servo channel set to " + str(self.gripper))

        self.pwm.setPWMFreq(50)         # recommended PWM frequency for the servos
        self.openGripper()              # at the start of any cycle open the gripper

        self.goDirectlyTo(0, 100, 50)   #   go to the 'home' position

        if self.debug:
            print ("gripper opened and positioned at 0, 100, 50 as a start position")

    	
    def setupServo(self, n_min, n_max, a_min, a_max):

        """Calculate servo calibration record to place in self.servoInfo"""
        # eg self.servoInfo["base"] = self.setupServo(145, 49, -pi/4, pi/4) sets up the 'base' servo record with the default values

        rec = {}
        n_range = n_max - n_min
        a_range = a_max - a_min
        if a_range == 0: return
        gain = n_range / a_range
        zero = n_min - gain * a_min
        rec["gain"] = gain
        rec["zero"] = zero
        rec["min"] = n_min
        rec["max"] = n_max

        if self.debug:
            print ("gain : " + str(gain))
            print ("zero : " + str(zero))
            print ("n_min: " + str(n_min))
            print ("n_max: " + str(n_max))

        return rec

    
    def angle2pwm(self, servo, angle):

        """Work out pulse length to use to achieve a given requested angle taking into account stored calibration data"""

        ret = 150 + int(0.5 + (self.servoInfo[servo]["zero"] + self.servoInfo[servo]["gain"] * angle) * 450 / 180)

        if self.debug:
            print ("servo        : " + str(servo))
            print ("angle        : " + str(angle))
            print ("pulse length : " + str(ret))


        return ret

    	
    def goDirectlyTo(self, x, y, z):

        """Set servo angles so as to place the gripper at a given Cartesian point as quickly as possible, without caring what path it takes to get there"""

        angles = [0,0,0]
        solvedebug=False
        if self.debug: solvedebug=True
        if kinematics.solve(x, y, z, angles, solvedebug):
            radBase = angles[0]
            radShoulder = angles[1]
            radElbow = angles[2]
            self.pwm.setPWM(self.base, 0, self.angle2pwm("base", radBase))
            self.pwm.setPWM(self.shoulder, 0, self.angle2pwm("shoulder", radShoulder))
            self.pwm.setPWM(self.elbow, 0, self.angle2pwm("elbow", radElbow))
            self.x = x
            self.y = y
            self.z = z
            if self.debug: print ("goto intermediate point %s" % ([x,y,z]))

    		
    def gotoPoint(self, x, y, z):

        """Travel in a straight line from current position to a requested position"""

        # can only be called after an initial movement otherwise the previous/current position is not known
        x0 = self.x
        y0 = self.y
        z0 = self.z
        dist = kinematics.distance(x0, y0, z0, x, y, z)
        if self.debug:
            print ("distance ")
        step = 1
        i = 0
        while i < dist:
    	    self.goDirectlyTo(x0 + (x - x0) * i / dist, y0 + (y - y0) * i / dist, z0 + (z - z0) * i / dist)
    	    time.sleep(0.01)  # damper interval to make movement slower: no shorter than 0.01
    	    i += step
        self.goDirectlyTo(x, y, z)
        time.sleep(0.05)

    	
    def openGripper(self):

        """Open the gripper, dropping whatever is being carried"""

        self.pwm.setPWM(self.gripper, 0, self.angle2pwm("gripper", pi/4.0))
        if self.debug:
            print ("gripper opened")
        time.sleep(0.3)

	
    def closeGripper(self):

        """Close the gripper, grabbing onto anything that might be there"""

        self.pwm.setPWM(self.gripper, 0, self.angle2pwm("gripper", -pi/4.0))
        if self.debug:
            print ("gripper closed")
        time.sleep(0.3)

    
    def isReachable(self, x, y, z):

        """Returns True if the point is (theoretically) reachable by the gripper"""

        radBase = 0
        radShoulder = 0
        radElbow = 0
        solvedebug=False
        if self.debug: solvedebug=True
        radangles =[radBase, radShoulder, radElbow]
        return kinematics.solve(x, y, z, radangles, solvedebug)
        #return kinematics.solve(x, y, z, radBase, radShoulder, radElbow)

    
    def getPos(self):

        """Returns the current position of the gripper"""

        return [self.x, self.y, self.z]


