#Constant variables for each servo on Byte
#TAG FOR THE 12 SERVOS
#import numpy as np
# BACK LEGS
#   RIGHT LEGS
SERVO_BRR = 0

SERVO_BRP1 = 1

SERVO_BRP2 = 2

#   LEFT LEGS
SERVO_BLR = 3

SERVO_BLP1 = 4

SERVO_BLP2 = 5

# FRONT LEGS
#   RIGHT LEGS
SERVO_FRR = 6

SERVO_FRP1 = 7

SERVO_FRP2 = 8

#   LEFT LEGS
SERVO_FLR = 9

SERVO_FLP1 = 10

SERVO_FLP2 = 11

# STEPS
STEPS = 20

# DELAY
LOOP_DELAY = 30

# Left / right legs  directions flags
LEFT_FLAG = 1
RIGHT_FLAG = 0

# PI Value in degrees
PI_ANGL = 180

HALF = 2

# Zero value
ZERO = 0

# Fixed distance between servo links
# D1 distance between Pitch axes from the legs
D1 = 200
# D2 distance between Roll axes from the legs
D2 = 90
# DZ_HOME Floor Distance in the home position
DZ_HOME = 120

# Decimal Rounds (constant to limit the decimals)
ROUND = 5

# - CONSTANTS FOR VISION PART
K_SIZE = 5

#Standard deviation for a gaussian for  X & Y
SIGMA_DEV = 50

#print(np.deg2rad(0))