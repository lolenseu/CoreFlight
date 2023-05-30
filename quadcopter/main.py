# [v0.1.7]

# -------------------- [Import from Library] --------------------
#import utime
import machine

from utime import sleep_ms
from machine import Pin,I2C
# -------------------- [~Import from Library] --------------------

# -------------------- [Import from Modules] --------------------



# -------------------- [~Import from Modules] --------------------

# -------------------- [Variables] --------------------
# ---------- [Basic Variables] ----------
# [Loop Tick]
tick_value=0

# [SDA, and SCL for I2C]
i2c_sda=0
i2c_scl=1
# ---------- [~Basic Variables] ----------

# ---------- [MPU6050 Sensor on I2C] ----------
# [MPU6050 address on I2C Bus]
mpu6050_addr=0x68

# [PWR_MGMT_1 memory address]
mpu6050_pwr_mgmt_1=0x6B

# [Accelerometer high and low register for each axis]
mpu6050_accel_xout_high=0x3B
mpu6050_accel_xout_low=0x3C
mpu6050_accel_yout_high=0x3D
mpu6050_accel_yout_low=0x3E
mpu6050_accel_zout_high=0x3F
mpu6050_accel_zout_low=0x40

# [Gyroscope high and low register for each axis]
mpu6050_gyro_xout_high=0x43
mpu6050_gyro_xout_low=0x44
mpu6050_gyro_yout_high=0x45
mpu6050_gyro_yout_low=0x46
mpu6050_gyro_zout_high=0x47
mpu6050_gyro_zout_low=0x48

# [Temperature high and low register]
mpu6050_temp_out_high = 0x41
mpu6050_temp_out_low = 0x42
# ---------- [~MPU6050 Sensor on I2C] ----------
# -------------------- [~Variables] --------------------

# -------------------- [Configuration Variables] --------------------
# [CPU Clock]
freq=256000000 # Hz == 256 MHz
#freq=128000000 # Hz == 128 MHz

# [MPU6050 Sensitivity for Acclerometer in LSB/g]
mpu6050_lsbg=16384.0 # LSB/g == +/-2g
#mpu6050_lsbg=8192.0 # LSB/g == +/-4g
#mpu6050_lsbg=4096.0 # LSB/g == +/-8g
#mpu6050_lsbg=2048.0 # LSB/g == +/-16g

# [MPU6050 Sensitivity for Gyroscope in LSB/dps]
mpu6050_lsbdps=131.0 # LSB/dps == +/-250 dps
#mpu6050_lsbdps=65.5 # LSB/dps == +/-500 dps
#mpu6050_lsbdps=32.8 # LSB/dps == +/-1000 dps
#mpu6050_lsbdps=16.4 # LSB/dps == +/-2000 dps
# -------------------- [~Configuration Variables] --------------------

# -------------------- [Functions] --------------------
# --------------- [MPU6050 Sensor Functions] ---------------
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

    accel_xaxis_high=i2c.readfrom_mem(mpu6050_addr,mpu6050_accel_xout_high,1)
    accel_xaxis_low=i2c.readfrom_mem(mpu6050_addr,mpu6050_accel_xout_low,1)
    accel_yaxis_high=i2c.readfrom_mem(mpu6050_addr,mpu6050_accel_yout_high,1)
    accel_yaxis_low=i2c.readfrom_mem(mpu6050_addr,mpu6050_accel_yout_low,1)
    accel_zaxis_high=i2c.readfrom_mem(mpu6050_addr,mpu6050_accel_zout_high,1)
    accel_zaxis_low=i2c.readfrom_mem(mpu6050_addr,mpu6050_accel_zout_low,1)

    accel_xaxis=combine_register_values(accel_xaxis_high,accel_xaxis_low)/mpu6050_lsbg
    accel_yaxis=combine_register_values(accel_yaxis_high,accel_yaxis_low)/mpu6050_lsbg
    accel_zaxis=combine_register_values(accel_zaxis_high,accel_zaxis_low)/mpu6050_lsbg
    
    return accel_xaxis,accel_yaxis,accel_zaxis

# [Get Gyroscope Values]
def mpu6050_get_gyro():
    global gyro_xaxis,gyro_yaxis,gyro_zaxis

    gyro_xaxis_high=i2c.readfrom_mem(mpu6050_addr,mpu6050_gyro_xout_high,1)
    gyro_xaxis_low=i2c.readfrom_mem(mpu6050_addr,mpu6050_gyro_xout_low,1)
    gyro_yaxis_high=i2c.readfrom_mem(mpu6050_addr,mpu6050_gyro_yout_high,1)
    gyro_yaxis_low=i2c.readfrom_mem(mpu6050_addr,mpu6050_gyro_yout_low,1)
    gyro_zaxis_high=i2c.readfrom_mem(mpu6050_addr,mpu6050_gyro_zout_high,1)
    gyro_zaxis_low=i2c.readfrom_mem(mpu6050_addr,mpu6050_gyro_zout_low,1)

    gyro_xaxis=combine_register_values(gyro_xaxis_high,gyro_xaxis_low)/mpu6050_lsbdps
    gyro_yaxis=combine_register_values(gyro_yaxis_high,gyro_yaxis_low)/mpu6050_lsbdps
    gyro_zaxis=combine_register_values(gyro_zaxis_high,gyro_zaxis_low)/mpu6050_lsbdps
    
    return gyro_xaxis,gyro_yaxis,gyro_zaxis

def mpu6050_get_temp():
    global temp_value

    temp_high=i2c.readfrom_mem(mpu6050_addr,mpu6050_temp_out_high,1)
    temp_low=i2c.readfrom_mem(mpu6050_addr,mpu6050_temp_out_low,1)

    temp_value=combine_register_values(temp_high,temp_low)/340.0+36.53

    return temp_value
# --------------- [~MPU6050 Sensor Functions] ---------------

# --------------- [Shell Print] ---------------
def shell_print():
    print("---------------------------------------------------------------------------")
    print("Raw")
    print("")
    print("MPU6050")
    print(f"Accel:\tXaxis= {accel_xaxis:.2f},\tYaxis= { accel_yaxis:.2f},\tZaxis= {accel_zaxis:.2f}")
    print(f"Gyro:\tXaxis= {gyro_xaxis:.2f},\tYaxis= {gyro_yaxis:.2f},\tZaxis= {gyro_zaxis:.2f}")
    print(f"Temp:\t{temp_value:.2f}°C")
    print("")
    print(f"Tick: {tick_value}")
    print("---------------------------------------------------------------------------")
# --------------- [~Shell Print] ---------------
# -------------------- [~Functions] --------------------

# -------------------- [Setup] --------------------
# [CPU Frequency]
machine.freq(freq)

# [Define I2C Bus]
i2c=I2C(0,sda=Pin(i2c_sda),scl=Pin(i2c_scl))

# [Initiate MPU6050 on I2C]
mpu6050_init(i2c)
# -------------------- [~Setup] --------------------

# -------------------- [Loop] --------------------
while True:
    # [Loop Tick]
    if tick_value==128:tick_value=0
    tick_value+=1

    # [MPU6050 Sensor Update]
    mpu6050_get_accel() # Accelerometer
    mpu6050_get_gyro() # Gyroscope
    mpu6050_get_temp() # Temperature


    # [Shell Print Update]
    shell_print()

    # [10 ms Delay]
    sleep_ms(10)
# -------------------- [~Loop] --------------------
