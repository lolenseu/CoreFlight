# ---------- [System] ----------
# Boot and Reboot
boot_state=1          # if set to zero need to manually boot on gpio14 (Pin14) to ground (GND)
reboot_state=0        # if set to one the flight controller will not going to bootup

# ---------- [CPU Frequency] ----------
# CPU Clock
freq=256000000 # Hz == 256 MHz
#freq=128000000 # Hz == 128 MHz

# ---------- [MPU6050 Sensitivity] ----------
# MPU6050 Sensitivity for Accelerometer in LSB/g]
accel_lsbg=16384.0 # LSB/g == +/-2g
#accel_lsbg=8192.0 # LSB/g == +/-4g
#accel_lsbg=4096.0 # LSB/g == +/-8g
#accel_lsbg=2048.0 # LSB/g == +/-16g

# MPU6050 Sensitivity for Gyroscope in LSB/dps]
gyro_lsbdps=131.0 # LSB/dps == +/-250 dps
#gyro_lsbdps=65.5 # LSB/dps == +/-500 dps
#gyro_lsbdps=32.8 # LSB/dps == +/-1000 dps
#gyro_lsbdps=16.4 # LSB/dps == +/-2000 dps
