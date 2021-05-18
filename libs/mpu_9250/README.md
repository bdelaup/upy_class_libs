# Purpose 
This an wrapper of the mpu_9250 driver available here [micropython-mpu9250](https://github.com/tuupola/micropython-mpu9250) by tuupola
Designed for educational purpose only

# Usage
## Basics

```python
from mpu import MPU
if __name__ == "__main__":
    i2c = I2C(id=1, scl=Pin(27), sda=Pin(26))
    mpu = MPU(i2c)
    while(True):
        print ("Acceleration :", mpu.acceleration_x, mpu.acceleration_y, mpu.acceleration_z)
        print ("Giroscope :", mpu.giro_x, mpu.giro_y, mpu.giro_z)
        print ("Temperature :", mpu.temperature)
        print ("")
        time.sleep_ms(1000)
        
```

## Calibration
Calibration value can be obtained by calling de calibration method
```python
from mpu import MPU
if __name__ == "__main__":
    i2c = I2C(id=1, scl=Pin(27), sda=Pin(26))
    mpu = MPU(i2c)
    mpu.calibrate()       
```

Then calibration values can passed as arguments to MPU constructor
```python
i2c = I2C(id=1, scl=Pin(27), sda=Pin(26),                  
        offset_default=( 0 , 0 , 0 ), # replace by values obtained using calibration method
        scale_default=( 1 , 1 , 1 )) # replace by values obtained using calibration method
```

## Advanced
Constructor options and defaults are
```python
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
```

# Licence
(c) B. Delaup
Licence GPL 3.0
