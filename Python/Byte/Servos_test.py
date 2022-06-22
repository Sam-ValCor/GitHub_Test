#Home_Byte
import constants as cnts
import  servos_functions as ser_fu
from adafruit_servokit import ServoKit
import time

# channel of the servo device (16)
# To chance frequency go to library adafruit_servokit.py in 81 line
my_servo_kit = ServoKit(channels=16)


# array for the tag servos 0-11
arrayServos = list([cnts.SERVO_BRR, cnts.SERVO_BRP1, cnts.SERVO_BRP2,
                    cnts.SERVO_BLR, cnts.SERVO_BLP1, cnts.SERVO_BLP2,
                    cnts.SERVO_FRR, cnts.SERVO_FRP1, cnts.SERVO_FRP2,
                    cnts.SERVO_FLR, cnts.SERVO_FLP1, cnts.SERVO_FLP2])

arrayHomeVal = [95, 75, 135, 106, 100, 55, 87, 80, 115, 75, 105, 50]
arrayDownVal = [95, 55, 155, 106, 125, 35, 87, 60, 135, 75, 125, 30]
arrayCurrentPos = [95, 75, 135, 106, 100, 55, 87, 80, 115, 75, 105, 50]
arrayStepVal = [0] * 12
steps = 20

# Pulse width in counts for 0° position and 180°
pos_0 = 172
pos_180 = 565
# transform tu unsigned add 2 elevated to 32 - 1
# u_pos_0 = pos_0 + (1 << 32)
# u_pos180 = pos180 + (1 << 32)

# posReach = False
# my_servo_kit.servo[0].set_pulse_width_range()

# function to set the corresponded angle for each servo

ser_fu.goHome(pos_0, pos_180)


while True:
    for idx in range(cnts.ZERO, 12, 1):
        # print(idx)
        arrayStepVal[idx] = ser_fu.Step(arrayCurrentPos[idx], arrayDownVal[idx], steps)
        # print(arrayStepVal)
    ser_fu.sendSteps(steps, arrayStepVal, arrayCurrentPos, arrayServos, pos_0, pos_180)
    time.sleep(1.50)

    for idx in range(cnts.ZERO, 12, 1):
        # print(idx)
        arrayStepVal[idx] = ser_fu.Step(arrayCurrentPos[idx], arrayHomeVal[idx], steps)
        print(arrayStepVal)
    ser_fu.sendSteps(steps, arrayStepVal, arrayCurrentPos, arrayServos, pos_0, pos_180)
    time.sleep(1.5)


# print(pos_0, pos180)