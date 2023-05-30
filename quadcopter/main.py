# [v0.1.5]

# -------------------- [Import from Library] --------------------
#import utime
import _thread

from utime import sleep_ms
from machine import Pin,I2C

# -------------------- [~Import from Library] --------------------

# -------------------- [Import from Modules] --------------------



# -------------------- [~Import from Modules] --------------------

# -------------------- [Variables] --------------------
# ---------- [Basic Variables] ----------
# [Loop Tick]
count=0

# [CPU Clock]
freq=256000000

# [SDA, and SCL for I2C]
i2c_sda=0
i2c_scl=1
# ---------- [~Basic Variables] ----------

# ---------- [MPU6050 Dvice on I2C] ----------
# [MPU6050 address on I2C Bus]
mpu6050_addr=0x68

# [PWR_MGMT_1 memory address]
mpu6050_pwr_mgmt_1=0x6B

# [Accelerometer high and low register for each axis]
mpu6050_accel_xaxis_high=0x3B
mpu6050_accel_xaxis_low=0x3C
mpu6050_accel_yaxis_high=0x3D
mpu6050_accel_yaxis_low=0x3E
mpu6050_accel_zaxis_high=0x3F
mpu6050_accel_zaxis_low=0x40

# [Gyroscope high and low register for each axis]
mpu6050_gyro_xaxis_high=0x43
mpu6050_gyro_xaxis_low=0x44
mpu6050_gyro_yaxis_high=0x45
mpu6050_gyro_yaxis_low=0x46
mpu6050_gyro_zaxis_high=0x47
mpu6050_gyro_zaxis_low=0x48

# [Accelerometer's LSB/g (least significant bits per gravitational force) sensitivity]
mpu6050_lsbg = 16384.0

# [Gyroscope's LSB/g sensitivity]
mpu6050_lsbds = 131.0 
# ---------- [~MPU6050 Dvice on I2C] ----------
# -------------------- [~Variables] --------------------

# -------------------- [Configuration File] --------------------



# -------------------- [~Configuration File] --------------------

# -------------------- [Functions] --------------------
# --------------- [MPU6050 Device Functions] ---------------
# [Set all bits in the PWR_MGMT_1 register to 0]
def mpu6050_init(i2c):
    i2c.writeto_mem(mpu6050_addr,mpu6050_pwr_mgmt_1,b'\x00')

# [Combine the values of high and low]
def combine_register_values(high,low):
    if not high[0]&0x80:
        return high[0]<<8|low[0]
    return -((high[0]^255)<<8)|(low[0]^255)+1

# [Get Accelerometer Values]
def mpu6050_get_accel():
    global accel_xaxis,accel_yaxis,accel_zaxis

    accel_xaxis_high=i2c.readfrom_mem(mpu6050_addr,mpu6050_accel_xaxis_high,1)
    accel_xaxis_low=i2c.readfrom_mem(mpu6050_addr,mpu6050_accel_xaxis_low,1)
    accel_yaxis_high=i2c.readfrom_mem(mpu6050_addr,mpu6050_accel_yaxis_high,1)
    accel_yaxis_low=i2c.readfrom_mem(mpu6050_addr,mpu6050_accel_yaxis_low,1)
    accel_zaxis_high=i2c.readfrom_mem(mpu6050_addr,mpu6050_accel_zaxis_high,1)
    accel_zaxis_low=i2c.readfrom_mem(mpu6050_addr,mpu6050_accel_zaxis_low,1)

    accel_xaxis=combine_register_values(accel_xaxis_high,accel_xaxis_low)/mpu6050_lsbg
    accel_yaxis=combine_register_values(accel_yaxis_high,accel_yaxis_low)/mpu6050_lsbg
    accel_zaxis=combine_register_values(accel_zaxis_high,accel_zaxis_low)/mpu6050_lsbg
    
    return accel_xaxis,accel_yaxis,accel_zaxis

# [Get Gyroscope Values]
def mpu6050_get_gyro():
    global gyro_xaxis,gyro_yaxis,gyro_zaxis

    gyro_xaxis_high=i2c.readfrom_mem(mpu6050_addr,mpu6050_gyro_xaxis_high,1)
    gyro_xaxis_low=i2c.readfrom_mem(mpu6050_addr,mpu6050_gyro_xaxis_low,1)
    gyro_yaxis_high=i2c.readfrom_mem(mpu6050_addr,mpu6050_gyro_yaxis_high,1)
    gyro_yaxis_low=i2c.readfrom_mem(mpu6050_addr,mpu6050_gyro_yaxis_low,1)
    gyro_zaxis_high=i2c.readfrom_mem(mpu6050_addr,mpu6050_gyro_zaxis_high,1)
    gyro_zaxis_low=i2c.readfrom_mem(mpu6050_addr,mpu6050_gyro_zaxis_low,1)

    gyro_xaxis=combine_register_values(gyro_xaxis_high,gyro_xaxis_low)/mpu6050_lsbds
    gyro_yaxis=combine_register_values(gyro_yaxis_high,gyro_yaxis_low)/mpu6050_lsbds
    gyro_zaxis=combine_register_values(gyro_zaxis_high,gyro_zaxis_low)/mpu6050_lsbds
    
    return gyro_xaxis,gyro_yaxis,gyro_zaxis
# --------------- [~MPU6050 Device Functions] ---------------

# --------------- [Shell Print] ---------------
def shell_print():
    print("")
    print("Raw")
    print(f"Accel:\tXaxis= {accel_xaxis:.2f},\tYaxis={ accel_yaxis:.2f},\tZaxis= {accel_zaxis:.2f}")
    print(f"Gyro:\tXaxis= {gyro_xaxis:.2f},\tYaxis= {gyro_yaxis:.2f},\tZaxis= {gyro_zaxis:.2f}")
    print("")

# --------------- [~Shell Print] ---------------
# -------------------- [~Functions] --------------------

# -------------------- [Setup] --------------------
# [Define I2C Bus]
i2c=I2C(0,sda=Pin(i2c_sda),scl=Pin(i2c_scl))

# [Initiate MPU6050 on I2C]
mpu6050_init(i2c)
# -------------------- [~Setup] --------------------

# -------------------- [Loop] --------------------
while True:
    # [Loop Tick]
    if count==100:count=0
    count+=1

    # [MPU6050 Update]
    mpu6050_get_accel() # Accelerometer
    mpu6050_get_gyro() # Gyroscope


    # [Shell Print Update]
    shell_print()

    # [10 ms Delay]
    sleep_ms(10)
    pass
# -------------------- [~Loop] --------------------
