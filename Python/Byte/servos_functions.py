import constants as cnts
import my_map
from adafruit_servokit import ServoKit
import time


# channel of the servo device (16)
# To chance frequency go to library adafruit_servokit.py in 81 line
myservoKit = ServoKit(channels=16)

posReach = False

# function to set the corresponded angle for each servo


def setServo(n_servo, angle, pos_i, pos_f):
    duty = my_map._map(angle, cnts.ZERO, cnts.PI_ANGL, pos_i, pos_f)
    # print(duty)
    #myservoKit.servo[n_servo].set_pulse_width_range(cnts.ZERO, duty)
    myservoKit.servo[n_servo].angle = angle
    #print(myservoKit.servo[n_servo].set_pulse_width_range(cnts.ZERO, duty))


def Step (init_Val, final_val, steps_amounts):
    # print(init_Val, final_val, steps_amounts)
    return int((final_val - init_Val) / steps_amounts)


def sendSteps (steps_amount, step_Val, current_val, arrayServos, pos_i, pos_f):
    for i in range(0, steps_amount, 1):
        for iservo in range(0, 12, 1):
            current_val[iservo] += step_Val[iservo]
            # print(current_val)
            setServo(arrayServos[iservo], current_val[iservo], pos_i, pos_f)
        time.sleep(cnts.LOOP_DELAY / 1000)
    posReach = True

# defined values for position
# 95, 75, 135, 106, 100, 55, 87, 80, 115, 75, 105, 50
def goHome(pos_i, pos_f):
    setServo(cnts.SERVO_BRR, 93, pos_i, pos_f)
    setServo(cnts.SERVO_BLR, 106, pos_i, pos_f)
    setServo(cnts.SERVO_FRR, 87, pos_i, pos_f)
    setServo(cnts.SERVO_FLR, 75, pos_i, pos_f)

    setServo(cnts.SERVO_BRP1, 75, pos_i, pos_f)
    setServo(cnts.SERVO_BLP1, 100, pos_i, pos_f)
    setServo(cnts.SERVO_FRP1, 80, pos_i, pos_f)
    setServo(cnts.SERVO_FLP1, 105, pos_i, pos_f)

    setServo(cnts.SERVO_BRP2, 135, pos_i, pos_f)
    setServo(cnts.SERVO_BLP2, 55, pos_i, pos_f)
    setServo(cnts.SERVO_FRP2, 115, pos_i, pos_f)
    setServo(cnts.SERVO_BRR, 50, pos_i, pos_f)


def goPaw(pos_i, pos_f):
    setServo(cnts.SERVO_BRR, 93, pos_i, pos_f)
    setServo(cnts.SERVO_BLR, 102, pos_i, pos_f)
    setServo(cnts.SERVO_FRR, 87, pos_i, pos_f)
    setServo(cnts.SERVO_FLR, 70, pos_i, pos_f)

    setServo(cnts.SERVO_BRP1, 60, pos_i, pos_f)
    setServo(cnts.SERVO_BLP1, 120, pos_i, pos_f)
    setServo(cnts.SERVO_FRP1, 170, pos_i, pos_f)
    setServo(cnts.SERVO_FLP1, 85, pos_i, pos_f)

    setServo(cnts.SERVO_BRP2, 150, pos_i, pos_f)
    setServo(cnts.SERVO_BLP2, 40, pos_i, pos_f)
    setServo(cnts.SERVO_FRP2, 180, pos_i, pos_f)
    setServo(cnts.SERVO_BRR, 90, pos_i, pos_f)