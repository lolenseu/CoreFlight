# [v0.1.2]

# -------------------- [import from library] --------------------
#import utime
import _thread

from utime import*
from machine import*

# -------------------- [~import from library] --------------------

# -------------------- [import from modules] --------------------



# -------------------- [~import from modules] --------------------

# -------------------- [configuration file] --------------------



# -------------------- [~configuration file] --------------------

# -------------------- [functions] --------------------
# --------------- [shell print] ---------------


# --------------- [~shell print] ---------------
# -------------------- [~functions] --------------------

# -------------------- [variables] --------------------
# ---------- [mpu6050 device over i2c] ----------

# [mpu6050 address on i2c bus]
mpu6050_addr=0x6B

# [pwr_mgmt_1 memory address]
mpu6050_pwr_mgmt_1=0x6B

# [accelerometer high and low register for each axis]
mpu6050_acc_xaxis_out_high=0x3B
mpu6050_acc_xaxis_out_low=0x3C
mpu6050_acc_yaxis_out_high=0x3D
mpu6050_acc_yaxis_out_low=0x3E
mpu6050_acc_zxis_out_high=0x3F
mpu6050_acc_zxis_out_low=0x40

# [gyroscope high and low register for each axis]
mpu6050_gyr_xaxis_out_high=0x43
mpu6050_gyr_xaxis_out_low=0x44
mpu6050_gyr_yaxis_out_high=0x45
mpu6050_gyr_yaxis_out_low=0x46
mpu6050_gyr_zxis_out_high=0x47
mpu6050_gyr_zxis_out_low=0x48

# ---------- [~mpu6050 device over i2c] ----------
# -------------------- [~variables] --------------------

# -------------------- [setup] --------------------
# [define i2c bus]
i2c=I2C(0,sda=Pin(0),scl=Pin(1),freq=4000000)
# -------------------- [~setup] --------------------

# -------------------- [loop] --------------------
while True:
    sleep_ms(10)
    pass
# -------------------- [~loop] --------------------
