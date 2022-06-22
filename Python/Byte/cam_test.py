import numpy as np
import cv2 as cv

cv.namedWindow('Canny_Edge')

def nothing(x):
    pass

#cv.createTrackbar('Increase','Canny_Edge', 0, 255, nothing)
#cv.createTrackbar('Decrease','Canny_Edge', 0, 255, nothing)



face_ext_alg_cas = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_detec_alg  = cv.CascadeClassifier('haarcascade_eye.xml')
cap = cv.VideoCapture(0)
kernel = np.ones((5, 5), np.uint8)


while True:

    ret2, img = cap.read()
    # img= cv.blur(img,(3,3))
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    # smoothing filter
    img_gray = cv.GaussianBlur(img_gray, (5, 5), 50, 50)

    """
    # morphological operations
    img_gray = cv.erode(img_gray, kernel, iterations=1)
    img_gray = cv.morphologyEx(img_gray, cv.MORPH_OPEN, kernel)
    img_gray = cv.dilate(img_gray, kernel, iterations=1)
    #img_gray = cv.morphologyEx(img_gray, cv.MORPH_CLOSE, kernel)
    """
    # First algorithm for faces
    faceMScale = face_ext_alg_cas.detectMultiScale(img_gray, 1.2, 5)

    # inc = cv.getTrackbarPos('Increase', 'Canny_Edge')
    # dec = cv.getTrackbarPos('Decrease', 'Canny_Edge')
    inc = 19
    dec = 36
    #img = cv.imread("naruto.jpg")

    # size of the image
    canny_edge = cv.Canny(img_gray, inc, dec)
    width = np.size(canny_edge, 1) / 2
    height = np.size(canny_edge, 0) / 2

    # cv.imshow('Canny_Edge_cam',canny_edge)
    for (x, y, w, h) in faceMScale:

        # x & y are the top left coordinates
        # y goes to 0 (up) a max val (down)
        rect = cv.rectangle(canny_edge, (x, y), (x + w, y + h), (50, 0, 100), 4)
        """ Moment = cv.moments(x,y)
        if Moment["m00"] == 0: Moment["m00"] = 1
        x1 = int(Moment["m10"] / Moment["m00"])
        y1 = int(Moment["m01"] / Moment["m00"])
        #cv.circle(img, (x1, y1), 5, (18, 156, 243), -1)
         """
        r_gray = img_gray[y:y + h, x:x + w]
        r_color = canny_edge[y:y + h, x:x + w]
        eyes = eye_detec_alg.detectMultiScale(r_color, 1.2, 5)

        for (ex, ey, ew, eh) in eyes:
            cv.rectangle(r_color, (ex, ey), (ex + ew, ey + eh), (50, 0, 100), 4)

        # draw of the center circle
        x_cent = int(x + w / 2)
        y_cent = int(y + h / 2)
        circles = cv.circle(canny_edge, (x_cent, y_cent), 3, (50, 0, 100), 4)

        # error for the centroid
        x_error = x_cent - width
        y_error = height - y_cent

    if len(faceMScale) == 0:
        x_error = 0
        y_error = 0


    print(x_error, y_error)
    cv.imshow('Canny_Edge', canny_edge)
    # print("X:", x, " Y: ", y, " W: ", w, "H: ", h)
    if cv.waitKey(1) == ord('e'):
       cv.destroyAllWindows()
       break

#img.show()
cap.release()
cv.destroyAllWindows()
