# -*- coding: utf-8 -*
'''!
  @file df_robot_ozone.py
  @brief Define the basic structure of the DFRobot_Ozone class, the implementation of the basic methods
  @copyright Copyright (c) 2010 DFRobot Co.Ltd (http://www.dfrobot.com)
  @license The MIT License (MIT)
  @author [ZhixinLiu](zhixin.liu@dfrobot.com) & revised for micropython by B. Delaup tested on Rpi Pico

'''

from machine import Pin, I2C, SoftI2C
from utime import *

OZONE_ADDRESS_0           = 0x70
OZONE_ADDRESS_1           = 0x71
OZONE_ADDRESS_2           = 0x72
OZONE_ADDRESS_3           = 0x73

## active  mode
MEASURE_MODE_AUTOMATIC    = 0x00
## passive mode
MEASURE_MODE_PASSIVE      = 0x01
## auto read ozone data
AUTO_READ_DATA            = 0x00
## passive read ozone data
PASSIVE_READ_DATA         = 0x01
## mode register
MODE_REGISTER             = 0x03
## read ozone data register
SET_PASSIVE_REGISTER      = 0x04
## auto data high eight bits
AUTO_DATA_HIGE_REGISTER   = 0x09
## auto data Low  eight bits
AUTO_DATA_LOW_REGISTER    = 0x0A
## auto data high eight bits
PASS_DATA_HIGE_REGISTER   = 0x07
## auto data Low  eight bits
PASS_DATA_LOW_REGISTER    = 0x08


class DFRobot_Ozone(object):
  ## mode flag
  __m_flag   = 0
  ## acquisition count
  __count    = 0
  ## iic send buffer
  __txbuf      = [0]
  ## ozone data
  __ozonedata  = [0]*101
  def __init__(self ,bus):
    self.i2cbus = bus

  def set_mode(self ,mode):
    '''!
      @brief set the mode
      @param MEASURE_MODE_AUTOMATIC  active mode
      @param MEASURE_MODE_PASSIVE    passive mode
    '''
    if mode ==  MEASURE_MODE_AUTOMATIC:
      __m_flag = 0
      self.__txbuf[0] = MEASURE_MODE_AUTOMATIC 
      self.write_reg(MODE_REGISTER ,self.__txbuf)
    elif mode == MEASURE_MODE_PASSIVE:
      __m_flag = 1
      self.__txbuf[0] = MEASURE_MODE_PASSIVE
      self.write_reg(MODE_REGISTER ,self.__txbuf)
    else:
      __m_flag = 2
      return

  def get_ozone_data(self ,collectnum):
    '''!
      @brief get the ozone data
      @param collectnum Collect the number
      @return ozone concentration, (units PPB)
    '''
    if collectnum > 0:
      for num in range(collectnum ,1 ,-1):
        self.__ozonedata[num-1] = self.__ozonedata[num-2]
      if self.__m_flag == 0:
        self.__txbuf[0] = AUTO_READ_DATA
        self.write_reg(SET_PASSIVE_REGISTER ,self.__txbuf)
        self.__ozonedata[0] = self.get_ozone(AUTO_DATA_HIGE_REGISTER)
      elif self.__m_flag == 1:
        self.__txbuf[0] = PASSIVE_READ_DATA
        self.write_reg(SET_PASSIVE_REGISTER ,self.__txbuf)
        self.__ozonedata[0] = self.get_ozone(PASS_DATA_HIGE_REGISTER)
      if self.__count < collectnum:
        self.__count += 1
      return self.get_average_num(self.__ozonedata ,self.__count)
    elif (collectnum > 100) or (collectnum <= 0):
      return -1
  
  def get_average_num(self ,barry ,Len):
    temp = 0
    for num in range (0 ,Len):
      temp += barry[num]
    return (temp / Len)

  def get_ozone(self,reg):
    rslt = self.read_reg(reg ,2)
    return ((rslt[0] << 8) + rslt[1])

class DFRobot_Ozone_IIC(DFRobot_Ozone): 
  def __init__(self ,bus ,addr):
    self.__addr = addr
    super(DFRobot_Ozone_IIC, self).__init__(bus)

  def write_reg(self, reg, data):
      self.i2cbus.writeto_mem(self.__addr , reg, bytes(data))

  def read_reg(self, reg ,l):
    rslt = self.i2cbus.readfrom_mem(self.__addr , reg, l)
#     print(rslt, list(rslt), (rslt[0] << 8) + rslt[1])
    return rslt

def test1():
    COLLECT_NUMBER=100
    i2c = SoftI2C(scl=Pin(20), sda=Pin(21), freq=200000)          
    sensor = DFRobot_Ozone_IIC(i2c, OZONE_ADDRESS_3)
    sensor.set_mode(MEASURE_MODE_AUTOMATIC)
    while True:
        data = sensor.get_ozone_data(COLLECT_NUMBER)
        print (data, "ppb") # Particules par miliard
        sleep_ms(1000)
        
def test2():
    COLLECT_NUMBER=100
    while True:
        try:
            i2c = SoftI2C(scl=Pin(20), sda=Pin(21), freq=200000)          
            sensor = DFRobot_Ozone_IIC(i2c, OZONE_ADDRESS_3)
            sensor.set_mode(MEASURE_MODE_AUTOMATIC)
            while True:
                data = sensor.get_ozone_data(COLLECT_NUMBER)
                print (data, "ppb") # Particules par miliard
                sleep_ms(1000)
                
        except Exception as e:
            sleep_ms(1000)
            print(e)

if __name__ == "__main__":
    test2()
            
               
        
        
        
