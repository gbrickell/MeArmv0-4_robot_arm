#!/usr/bin/python

# updates in July 2018 to use python 3 and to remove option to auto set the busnum/port
#  further updates for use with the Raspberry Pi Maker Kit in Nov'21
# based upon the code from York Hack Space May 2014
# downloaded from https://github.com/RorschachUK/meArmPi

# this file should be in the same folder as the test code

import smbus

# ===========================================================================
# PCA9685_I2C Class
# ===========================================================================

class PCA9685_I2C :

  @staticmethod
  def getPiRevision():
    "Gets the version number of the Raspberry Pi board"
    # Courtesy quick2wire-python-api
    # https://github.com/quick2wire/quick2wire-python-api

    # this function has been left in place BUT it no longer works with the wider range of RPis now available

    try:
      with open('/proc/cpuinfo','r') as f:
        for line in f:
          if line.startswith('Revision'):
            return 1 if int(line.rstrip()[-4:]) < 3 else 2   # negative index means count from the right
    except:
      return 0

  @staticmethod
  def getPiI2CBusNumber():
    # Gets the I2C bus number /dev/i2c#
    return 1 if PCA9685_I2C.getPiRevision() > 1 else 0
 
  def __init__(self, address, busnum=-1, debug=False):
    self.address = address
    # By default, the correct I2C bus is auto-detected using /proc/cpuinfo
    # Alternatively, you can hard-code the bus version below:
    # self.bus = smbus.SMBus(0); # Force I2C0 (early 256MB Pi's)

    # Always force the use of the I2C-1 port used with later versions of the RPi because
    #  the auto set routine does not work with the wider range of RPi's now available
    self.bus = smbus.SMBus(1); # Force I2C1 (512MB Pi's) - actually ALL RPi's since 2012
    # self.bus = smbus.SMBus(busnum if busnum >= 0 else PCA9685_I2C.getPiI2CBusNumber())
    self.debug = debug

  def reverseByteOrder(self, data):
    "Reverses the byte order of an int (16-bit) or long (32-bit) value"
    # Courtesy Vishal Sapre
    byteCount = len(hex(data)[2:].replace('L','')[::2])
    val       = 0
    for i in range(byteCount):
      val    = (val << 8) | (data & 0xff)
      data >>= 8
    return val

  def errMsg(self):
    print ("Error accessing 0x%02X: Check your I2C address" % self.address)
    return -1

  def write8(self, reg, value):
    "Writes an 8-bit value to the specified register/address"
    try:
      self.bus.write_byte_data(self.address, reg, value)
      if self.debug:
        print ("I2C: Wrote 0x%02X to register 0x%02X" % (value, reg))
    except (IOError, err):
      return self.errMsg()

  def write16(self, reg, value):
    "Writes a 16-bit value to the specified register/address pair"
    try:
      self.bus.write_word_data(self.address, reg, value)
      if self.debug:
        print ("I2C: Wrote 0x%02X to register pair 0x%02X,0x%02X" % (value, reg, reg+1))
    except (IOError, err):
      return self.errMsg()

  def writeList(self, reg, list):
    "Writes an array of bytes using I2C format"
    try:
      if self.debug:
        print ("I2C: Writing list to register 0x%02X:" % reg)
        print (list)
      self.bus.write_i2c_block_data(self.address, reg, list)
    except (IOError, err):
      return self.errMsg()

  def readList(self, reg, length):
    "Read a list of bytes from the I2C device"
    try:
      results = self.bus.read_i2c_block_data(self.address, reg, length)
      if self.debug:
        print ("I2C: Device 0x%02X returned the following from reg 0x%02X" %
         (self.address, reg))
        print (results)
      return results
    except (IOError, err):
      return self.errMsg()

  def readU8(self, reg):
    "Read an unsigned byte from the I2C device"
    try:
      result = self.bus.read_byte_data(self.address, reg)
      if self.debug:
        print ("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" %
         (self.address, result & 0xFF, reg))
      return result
    except (IOError, err):
      return self.errMsg()

  def readS8(self, reg):
    "Reads a signed byte from the I2C device"
    try:
      result = self.bus.read_byte_data(self.address, reg)
      if result > 127: result -= 256
      if self.debug:
        print ("I2C: Device 0x%02X returned 0x%02X from reg 0x%02X" %
         (self.address, result & 0xFF, reg))
      return result
    except (IOError, err):
      return self.errMsg()

  def readU16(self, reg):
    "Reads an unsigned 16-bit value from the I2C device"
    try:
      result = self.bus.read_word_data(self.address,reg)
      if (self.debug):
        print ("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % (self.address, result & 0xFFFF, reg))
      return result
    except (IOError, err):
      return self.errMsg()

  def readS16(self, reg):
    "Reads a signed 16-bit value from the I2C device"
    try:
      result = self.bus.read_word_data(self.address,reg)
      if (self.debug):
        print ("I2C: Device 0x%02X returned 0x%04X from reg 0x%02X" % (self.address, result & 0xFFFF, reg))
      return result
    except (IOError, err):
      return self.errMsg()

if __name__ == '__main__':
  try:
    bus = PCA9685_I2C(address=0)
    print ("Default I2C bus is accessible")
  except:
    print ("Error accessing default I2C bus")
