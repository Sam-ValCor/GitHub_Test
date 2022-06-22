import numpy as np
import cv2 as cv
import constants as cnts
import servos_functions as ser_fu
import ik_cal_main as ik_cal
import time
from adafruit_servokit import ServoKit

# - Computer Vision

# Development of window
#cv.namedWindow('Canny_Edge')

# To create a trackbar (Uncomment, if you are  testing) {
""""
def nothing(x):
    pass

cv.createTrackbar('Increase','Canny_Edge', 0, 255, nothing)
cv.createTrackbar('Decrease','Canny_Edge', 0, 255, nothing)
"""
# }

# Algorithms to detect faces (There are better alg than those)
face_ext_alg_cas = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_detec_alg  = cv.CascadeClassifier('haarcascade_eye.xml')

# capture video id = 0
cap = cv.VideoCapture(0)

# mask or convolution matrix size 5
kernel = np.ones((cnts.K_SIZE, cnts.K_SIZE), np.uint8)

# - Servo Motor

# channel of the servo device (16)
# To chance frequency go to library adafruit_servokit.py in 81 line
myservoKit = ServoKit(channels=16)

#array for the tag servos 0-11
arrayServos = list([cnts.SERVO_BRR, cnts.SERVO_BRP1, cnts.SERVO_BRP2,
                    cnts.SERVO_BLR, cnts.SERVO_BLP1, cnts.SERVO_BLP2,
                    cnts.SERVO_FRR, cnts.SERVO_FRP1, cnts.SERVO_FRP2,
                    cnts.SERVO_FLR, cnts.SERVO_FLP1, cnts.SERVO_FLP2])

# Setting arrays values for specif movements
arrayHomeVal = [95, 75, 135, 106, 100, 55, 87, 80, 115, 75, 105, 50]
arrayDownVal = [95, 55, 155, 106, 125, 35, 87, 60, 135, 75, 125, 30]
arrayCurrentPos = [95, 75, 135, 106, 100, 55, 87, 80, 115, 75, 105, 50]
arrayStepVal = [0] * 12
steps = 20


#Pulse width in counts for 0° position and 180°
pos_0 = 172
pos_180 = 565
#tranform tu unsigned add 2 elevated to 32 - 1
#u_pos_0 = pos_0 + (1 << 32)
#u_pos180 = pos180 + (1 << 32)

# posReach = False
# myservokit.servo[0].set_pulse_width_range()

# function to set the corresponded angle for each servo

#ser_fu.goHome(pos_0, pos_180)

while True:

    # Computer Vision part
    ret2, img = cap.read()
    # convert the input image to gray colour
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # A gaussianBlur for a smoothing filter
    img_gray = cv.GaussianBlur(img_gray, (cnts.K_SIZE, cnts.K_SIZE), cnts.SIGMA_DEV, cnts.SIGMA_DEV)

    # morphological operations to improve the filter (it can be erase)
    """
    img_gray = cv.erode(img_gray, kernel, iterations=1)
    img_gray = cv.morphologyEx(img_gray, cv.MORPH_OPEN, kernel)
    img_gray = cv.dilate(img_gray, kernel, iterations=1)
    img_gray = cv.morphologyEx(img_gray, cv.MORPH_CLOSE, kernel)
    """

    # First algorithm for faces
    faceMScale = face_ext_alg_cas.detectMultiScale(img_gray, 1.2, 5)

    # To set value for the canny edge method (border detector)
    # inc = cv.getTrackbarPos('Increase', 'Canny_Edge') # Uncomment Just for testing and set a value
    # dec = cv.getTrackbarPos('Decrease', 'Canny_Edge') # Uncomment Just for testing and set a value
    inc = 15
    dec = 24

    canny_edge = cv.Canny(img_gray, inc, dec)

    # image size x and y divided by 2 (default 640 x 480)
    width = np.size(canny_edge, 1) / cnts.HALF
    height = np.size(canny_edge, 0) / cnts.HALF

    # Start in home position
    # ser_fu.goHome(pos_0, pos_180)

    for (x, y, w, h) in faceMScale:

        # x & y are the top left coordinates
        # y goes to 0 (up) a max val (down)
        # To draw a square to visualize a face border
        # rect = cv.rectangle(canny_edge, (x, y), (x + w, y + h), (50, 0, 100), 4) # Uncomment Just for testing

        # Can be erase is to show eyes if you want
        r_gray = img_gray[y:y + h, x:x + w]
        r_color = canny_edge[y:y + h, x:x + w]
        eyes = eye_detec_alg.detectMultiScale(r_color, 1.2, 5)

        for (ex, ey, ew, eh) in eyes:
            cv.rectangle(r_color, (ex, ey), (ex + ew, ey + eh), (50, 0, 100), 4)

        # Centroid for the located face
        x_cent = int(x + w / 2)
        y_cent = int(y + h / 2)

        # To draw a circle to visualize the center mass in the detected face
        #circl = cv.circle(canny_edge, (x_cent, y_cent), 3, (50, 0, 100), 4) # Uncomment Just for testing

        # Error to fix the position and locate the object
        x_error = x_cent - width
        y_error = height - y_cent

    if len(faceMScale) == 0:
        x_error = 0
        y_error = 0

    k1 = -0.1
    k2 = - 0.1

    yaw_d = k1 * x_error
    pitch_d = k2 * y_error

    # Desired translation
    dx = 0
    dy = 0
    dz = -10

    # Desired orientation
    roll = np.deg2rad(0)
    # pitch = np.deg2rad(0.5 * roll_t(i))
    pitch = np.deg2rad(pitch_d)
    # yaw = np.deg2rad(0.5 * pitch_t(i))
    yaw = np.deg2rad(yaw_d)

    # Desired pose from the world respectively
    pose_d = np.float_([[dx], [dy], [dz], [roll], [pitch], [yaw]])

    # Initial - fixed feet position (coordinates)
    foot_lf = [[100], [70], [0], [1]]
    foot_rf = [[100], [-70], [0], [1]]
    foot_lb = [[-100], [70], [0], [1]]
    foot_rb = [[-100], [-70], [0], [1]]

    q_cal = ik_cal.ik_calc(pose_d, foot_lf, foot_rf, foot_lb, foot_rb)

    # qn's are the calculated angles for each servo of the legs
    # back right leg
    q1_rb = np.rad2deg(q_cal[9] + (np.pi / 2))  # -pi/2 < q1 < pi/2  # q1 servo roll
    q2_rb = np.rad2deg(- q_cal[10] + np.pi)  # 0 < q2 < pi # q2 servo pitch
    q3_rb = np.rad2deg(np.pi / 2 - q_cal[11] + q_cal[10])  # 0 < q3 < pi  # q3 servo pitch
    q_rb = [[q1_rb], [q2_rb], [q3_rb]]

    # back left leg
    q1_lb = np.rad2deg(-q_cal[6] + (np.pi / 2))  # -pi/2 < q1 < pi/2
    q2_lb = np.rad2deg(q_cal[7])  # 0 < q2 < pi
    q3_lb = np.rad2deg(np.pi / 2 - q_cal[8] + q_cal[7])  # 0 < q3 < pi
    q_lb = [[q1_lb], [q2_lb], [q3_lb]]

    # frontal right leg
    q1_rf = np.rad2deg(-q_cal[3] + (np.pi / 2))  # -pi/2 < q1 < pi/2
    q2_rf = np.rad2deg(-q_cal[4] + np.pi)  # 0 < q2 < pi
    q3_rf = np.rad2deg(np.pi / 2 - q_cal[5] + q_cal[4])  # 0 < q3 < pi
    q_rf = [[q1_rf], [q2_rf], [q3_rf]]

    # frontal left leg
    q1_lf = np.rad2deg(q_cal[0] + (np.pi / 2) )  # -pi/2 < q1 < pi/2
    q2_lf = np.rad2deg(q_cal[1])  # 0 < q2 < pi
    q3_lf = np.rad2deg(np.pi / 2 - q_cal[2] + q_cal[1])  # 0 < q3 < pi
    q_lf = [[q1_rb], [q2_rb], [q3_rb]]

    #  Desired Setting
    Q_d = [[q_lf], [q_rf], [q_lb], [q_rb]]
    """
    # Send angle position for each servo (It needs else conditions)
    # q_1s conditions -pi/2 < q1 < pi/2
    if q1_lf >= -90 or q1_lf <= 90:
        ser_fu.setServo(cnts.SERVO_FLR, q1_lf, pos_0, pos_180)
        time.sleep(cnts.LOOP_DELAY / 1000)
        
    if q1_rf >= -90 or q1_rf <= 90:
        ser_fu.setServo(cnts.SERVO_FRR, q1_rf, pos_0, pos_180)
        time.sleep(cnts.LOOP_DELAY / 1000)
        
    if q1_lb >= -90 or q1_lb <= 90:
        ser_fu.setServo(cnts.SERVO_BLR, q1_lb, pos_0, pos_180)
        time.sleep(cnts.LOOP_DELAY / 1000)
        
    if q1_rb >= -90 or q1_rb <= 90:
        ser_fu.setServo(cnts.SERVO_BRR, q1_rb, pos_0, pos_180)
        time.sleep(cnts.LOOP_DELAY / 1000)

    # q_2s conditions # 0 < q2 < pi
    if q2_lf >= 0 or q2_lf <= 180:
        ser_fu.setServo(cnts.SERVO_FLP1, q2_lf, pos_0, pos_180)
        time.sleep(cnts.LOOP_DELAY / 1000)

    if q2_rf >= 0 or q2_rf <= 180:
        ser_fu.setServo(cnts.SERVO_FRP1, q2_rf, pos_0, pos_180)
        time.sleep(cnts.LOOP_DELAY / 1000)

    if q2_lb >= 0 or q2_lb <= 180:
        ser_fu.setServo(cnts.SERVO_BLP1, q2_lb, pos_0, pos_180)
        time.sleep(cnts.LOOP_DELAY / 1000)

    if q2_rb >= 0 or q2_rb <= 180:
        ser_fu.setServo(cnts.SERVO_BRP1, q2_rb, pos_0, pos_180)
        time.sleep(cnts.LOOP_DELAY / 1000)

    # q_3s conditions 0 < q3 < pi
    if q3_rf >= 0 or q3_rf <= 180:
        ser_fu.setServo(cnts.SERVO_FRP2, q3_rf, pos_0, pos_180)
        time.sleep(cnts.LOOP_DELAY / 1000)

    if q3_lf >= 0 or q3_lf <= 180:
        ser_fu.setServo(cnts.SERVO_FLP2, q3_lf, pos_0, pos_180)
        time.sleep(cnts.LOOP_DELAY / 1000)
        
    if q3_lb >= 0 or q3_lb <= 180:
        ser_fu.setServo(cnts.SERVO_BLP2, q3_lb, pos_0, pos_180)
        time.sleep(cnts.LOOP_DELAY / 1000)

    if q3_rb >= 0 or q3_rb <= 180:
        ser_fu.setServo(cnts.SERVO_BRP2, q3_rb, pos_0, pos_180)
        time.sleep(cnts.LOOP_DELAY / 1000)
    """
    print(x_error, y_error, Q_d)
    """
     # cv.imshow('Canny_Edge',canny_edge)
     # print("X:", x, " Y: ", y, " W: ", w, "H: ", h)
     if cv.waitKey(1) == ord('e'):
        cv.destroyAllWindows()
        break
     """
    # img.show()
    # cap.release()
    # cv.destroyAllWindows()

    """
    for idx in range(cnts.ZERO, 12, 1):
        #print(idx)
        arrayStepVal[idx] = ser_fu.Step(arrayCurrentPos[idx], arrayDownVal[idx], steps)
        #print(arrayStepVal)
    ser_fu.sendSteps(steps, arrayStepVal, arrayCurrentPos, arrayServos, pos_0, pos_180)
    time.sleep(1.50)

    for idx in range(cnts.ZERO, 12, 1):
        #print(idx)
        arrayStepVal[idx] = ser_fu.Step(arrayCurrentPos[idx], arrayHomeVal[idx], steps)
        print(arrayStepVal)
    ser_fu.sendSteps(steps, arrayStepVal, arrayCurrentPos, arrayServos, pos_0, pos_180)
    time.sleep(1.5)
    """