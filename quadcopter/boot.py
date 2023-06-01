# This file is executed on every boot (including wake-boot from deepsleep)
#import esp
#esp.osdebug(None)
#import webrepl
#webrepl.start()

# v0.1.8
# ampy --h # Flash Tool

# ---------- [Library] ----------
import machine
import utime

# ---------- [Modules] ----------
from config import*

# ---------- [Define Variables] ----------
# CPU Temp
adc_temp=machine.ADC(4)

# SDA, and SCL for I2C
i2c_sda=0
i2c_scl=1

# Define I2C Bus
i2c=machine.I2C(0,sda=machine.Pin(i2c_sda),scl=machine.Pin(i2c_scl))

# [MPU6050] --------------------
# MPU6050 address on I2C Bus
addr=0x68

# PWR_MGMT_1 memory address
pwr_mgmt_1=0x6B

# Accelerometer high and low register for each axis
accel_xout_high=0x3B
accel_xout_low=0x3C
accel_yout_high=0x3D
accel_yout_low=0x3E
accel_zout_high=0x3F
accel_zout_low=0x40

# Gyroscope high and low register for each axis
gyro_xout_high=0x43
gyro_xout_low=0x44
gyro_yout_high=0x45
gyro_yout_low=0x46
gyro_zout_high=0x47
gyro_zout_low=0x48

# Temperature high and low register
temp_out_high = 0x41
temp_out_low = 0x42

# ---------- [Basic Variables] ----------
# Loop Tick
tick_value=0

# ---------- [Functions] ----------
# rp2040
class _rp2040:
    def __init__(self):
        pass

    def get_temp():
        global rp2040_temp
        read_adc_temp=adc_temp.read_u16()
        rp2040_temp=27-(read_adc_temp*3.3/(65535)-0.706)/0.001721
        return rp2040_temp

# mpu6050
class _mpu6050:
    def __inti__(self):
        pass

    # Set all bits in the PWR_MGMT_1 register to 0
    def init(i2c):
        i2c.writeto_mem(addr,pwr_mgmt_1,b'\x00')

    # Combine the values of high and low
    def combine_register_values(high,low):
        if not high[0]&0x80:
            return high[0]<<8|low[0]
        return -((high[0]^255)<<8)|(low[0]^255)+1

    # Get Accelerometer Values
    def get_accel():
        global accel_xaxis,accel_yaxis,accel_zaxis
        accel_xaxis_high=i2c.readfrom_mem(addr,accel_xout_high,1)
        accel_xaxis_low=i2c.readfrom_mem(addr,accel_xout_low,1)
        accel_yaxis_high=i2c.readfrom_mem(addr,accel_yout_high,1)
        accel_yaxis_low=i2c.readfrom_mem(addr,accel_yout_low,1)
        accel_zaxis_high=i2c.readfrom_mem(addr,accel_zout_high,1)
        accel_zaxis_low=i2c.readfrom_mem(addr,accel_zout_low,1)
        accel_xaxis=_mpu6050.combine_register_values(accel_xaxis_high,accel_xaxis_low)/accel_lsbg
        accel_yaxis=_mpu6050.combine_register_values(accel_yaxis_high,accel_yaxis_low)/accel_lsbg
        accel_zaxis=_mpu6050.combine_register_values(accel_zaxis_high,accel_zaxis_low)/accel_lsbg    
        return [accel_xaxis,accel_yaxis,accel_zaxis]

    # Get Gyroscope Values
    def get_gyro():
        global gyro_xaxis,gyro_yaxis,gyro_zaxis
        gyro_xaxis_high=i2c.readfrom_mem(addr,gyro_xout_high,1)
        gyro_xaxis_low=i2c.readfrom_mem(addr,gyro_xout_low,1)
        gyro_yaxis_high=i2c.readfrom_mem(addr,gyro_yout_high,1)
        gyro_yaxis_low=i2c.readfrom_mem(addr,gyro_yout_low,1)
        gyro_zaxis_high=i2c.readfrom_mem(addr,gyro_zout_high,1)
        gyro_zaxis_low=i2c.readfrom_mem(addr,gyro_zout_low,1)
        gyro_xaxis=_mpu6050.combine_register_values(gyro_xaxis_high,gyro_xaxis_low)/gyro_lsbdps
        gyro_yaxis=_mpu6050.combine_register_values(gyro_yaxis_high,gyro_yaxis_low)/gyro_lsbdps
        gyro_zaxis=_mpu6050.combine_register_values(gyro_zaxis_high,gyro_zaxis_low)/gyro_lsbdps  
        return [gyro_xaxis,gyro_yaxis,gyro_zaxis]

    # Get Temperature Values
    def get_temp():
        global mpu6050_temp
        temp_high=i2c.readfrom_mem(addr,temp_out_high,1)
        temp_low=i2c.readfrom_mem(addr,temp_out_low,1)
        mpu6050_temp=_mpu6050.combine_register_values(temp_high,temp_low)/340.0+36.53
        return mpu6050_temp

# shell
class _shell:
    def __init__(self) :
        pass
        
    def shell_print():
        print("---------------------------------------------------------------------------")
        print("Raw")
        print("")
        print("RP2040")
        print(f"Temp:\t{rp2040_temp:.2f}°C")
        print("")
        print("MPU6050")
        print(f"Accel:\tXaxis= {accel_xaxis:.2f},\tYaxis= {accel_yaxis:.2f},\tZaxis= {accel_zaxis:.2f}")
        print(f"Gyro:\tXaxis= {gyro_xaxis:.2f},\tYaxis= {gyro_yaxis:.2f},\tZaxis= {gyro_zaxis:.2f}")
        print(f"Temp:\t{mpu6050_temp:.2f}°C")
        print("")
        print(f"Tick: {tick_value}")
        print("---------------------------------------------------------------------------")

# main
class _main:
    def __init__(self):
        pass

    def loop():
        # Loop
        while True:
            # [Loop Tick]
            if tick_value==128:tick_value=0
            tick_value+=1

            # [RP2040 Serson Update]
            _rp2040.get_temp() # Temperature

            # [MPU6050 Sensor Update]
            _mpu6050.get_accel() # Accelerometer
            _mpu6050.get_gyro() # Gyroscope
            _mpu6050.get_temp() # Temperature


            # [Shell Print Update]
            _shell.shell_print()

            # 10 ms Delay
            utime.sleep_ms(10)


# ---------- [Setup] ----------
# CPU Frequency
machine.freq(freq)

# Initiate MPU6050 on I2C
_mpu6050.init(i2c)

# ---------- [Loop] ----------
_main.loop()

