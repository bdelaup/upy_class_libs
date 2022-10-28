import time
from microbit import i2c
from mpu9250 import MPU9250
from mpu6500 import MPU6500, SF_G, SF_DEG_S,
from mpu6500 import ACCEL_FS_SEL_2G, ACCEL_FS_SEL_4G, ACCEL_FS_SEL_8G, ACCEL_FS_SEL_16G
from mpu6500 import GYRO_FS_SEL_250DPS, GYRO_FS_SEL_500DPS, GYRO_FS_SEL_1000DPS, GYRO_FS_SEL_2000DPS
from ak8963 import AK8963

# i2c = I2C(id=1, scl=Pin(27), sda=Pin(26))

# mpu6500 = MPU6500(i2c, accel_sf=SF_G, gyro_sf=SF_DEG_S)
# sensor = MPU9250(i2c, mpu6500=mpu6500)    
    
class MPU:
    def __init__(self,
                 i2c,
                 accel_scale_factor=SF_G,     accel_func_scale=ACCEL_FS_SEL_2G,
                 gyro_scale_factor=SF_DEG_S,  gyro_func_scale=GYRO_FS_SEL_250DPS,
                 offset_default=( 0 , 0 , 0 ),
                 scale_default=( 1 , 1 , 1 )
                 ):
        """ SF scale factor -> facteur de mise à l'échelle (unites)
            accel_scale_factor : 
                SF_G = 1
                SF_M_S2 = 9.80665 # 1 g = 9.80665 m/s2 ie. standard gravity
                
            gyro_scale_factor : 
                SF_DEG_S = 1
                SF_RAD_S = 0.017453292519943 # 1 deg/s is 0.017453292519943 rad/s
               
            FS functionning scale : plage de mesure
            gyro_func_scale :
                ACCEL_FS_SEL_2G 
                ACCEL_FS_SEL_4G 
                ACCEL_FS_SEL_8G 
                ACCEL_FS_SEL_16G
            
            gyro_func_scale (deg/s):
                GYRO_FS_SEL_250DPS 
                GYRO_FS_SEL_500DPS 
                GYRO_FS_SEL_1000DPS
                GYRO_FS_SEL_2000DPS
                
            offset_default, offset_default : obtenu par la calibration
        """        
        self.mpu6500 = MPU6500(i2c,
                          accel_sf=accel_scale_factor, accel_fs = accel_func_scale,
                          gyro_sf=gyro_scale_factor, gyro_fs = gyro_func_scale)
        
        self.ak8963 = AK8963(i2c, offset = offset_default, scale = scale_default)
        #self.ak8963 = AK8963(i2c)        
        sensor = MPU9250(i2c, mpu6500=self.mpu6500, ak8963=self.ak8963)
        print("MPU9250 id: " + hex(sensor.whoami))
    
    def calibrate(self):
        print ("Orienter dans toutes les directions le temps de la calibration 200s")
        offset, scale = self.ak8963.calibrate(count=256, delay=200)
        print ("offset=(", offset[0],",", offset[1], ",",offset[2], ")")
        print ("scale=(", scale[0],",", scale[1], ",",scale[2], ")")
    
    @property
    def acceleration_x(self):
        return sensor.acceleration[0]
        
    @property
    def acceleration_y(self):
        return sensor.acceleration[1]
    
    @property
    def acceleration_z(self):
        return sensor.acceleration[2]
    
    @property
    def giro_x(self):
        return sensor.gyro[0]
    
    @property
    def giro_y(self):
        return sensor.gyro[1]
        
    @property
    def giro_z(self):
        return sensor.gyro[2]
    
    @property
    def champ_mag_x(self):
        return sensor.magnetic[0]
    
    @property
    def champ_mag_y(self):
        return sensor.magnetic[1]
    
    @property
    def champ_mag_z(self):
        return sensor.magnetic[2]
    
    @property
    def temperature(self):
        return sensor.temperature
    
if __name__ == "__main__":
    port_i2c = microbit.i2c
    mpu = MPU(i2c)
    #mpu.calibrate()
    while(True):
        print ("Acceleration :", mpu.acceleration_x, mpu.acceleration_y, mpu.acceleration_z)
        print ("Giroscope :", mpu.giro_x, mpu.giro_y, mpu.giro_z)
        print ("Temperature :", mpu.temperature)
        print ("")
        time.sleep_ms(1000)

