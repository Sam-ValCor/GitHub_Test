import numpy as np
import constants as cnts
import time
from adafruit_servokit import ServoKit

# channel of the servo device (16)
# To chance frequency go to library adafruit_servokit.py in 81 line
myservoKit = ServoKit(channels=16)

#array for the tag servos 0-11
arrayServos = list([cnts.SERVO_BRR, cnts.SERVO_BRP1, cnts.SERVO_BRP2,
                    cnts.SERVO_BLR, cnts.SERVO_BLP1, cnts.SERVO_BLP2,
                    cnts.SERVO_FRR, cnts.SERVO_FRP1, cnts.SERVO_FRP2,
                    cnts.SERVO_FLR, cnts.SERVO_FLP1, cnts.SERVO_FLP2])

for idx2 in range(0, 90, 1):
    myservoKit.servo[cnts.SERVO_BRP1].angle = idx2
    time.sleep(0.05)

myservoKit.servo[cnts.SERVO_BRP1].angle = 50.3
