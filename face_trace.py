import cv2

import numpy as np

from djitellopy import tello

import time
# Creating the drone object
drone = tello.Tello()
# connect to the drone
drone.connect()

print(drone.get_battery())
# Turning on the camera
drone.streamon()

drone.takeoff()

drone.send_rc_control(0, 0, 25, 0)

time.sleep(2.5)

width, height = 360, 240

fbRange = [6200, 6800]

pid = [0.4, 0.4, 0]

previous_error = 0


def find_face(img):
    face_cascade = cv2.CascadeClassifier("Resources/haarcascade_frontalface_default.xml")

    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(img_gray, 1.2, 8)

    my_face_list_c = []

    my_face_list_area = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

        cx = x + w // 2

        cy = y + h // 2

        area = w * h

        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)

        my_face_list_c.append([cx, cy])

        my_face_list_area.append(area)

    if len(my_face_list_area) != 0:

        i = my_face_list_area.index(max(my_face_list_area))

        return img, [my_face_list_c[i], my_face_list_area[i]]

    else:

        return img, [[0, 0], 0]


def track_face(info, width, pid, pError):
    area = info[1]

    x, y = info[0]

    fb = 0

    error = x - width // 2

    speed = pid[0] * error + pid[1] * (error - pError)

    speed = int(np.clip(speed, -100, 100))

    if area > fbRange[0] and area < fbRange[1]:

        fb = 0

    elif area > fbRange[1]:

        fb = -20

    elif area < fbRange[0] and area != 0:

        fb = 20

    if x == 0:
        speed = 0

        error = 0

    drone.send_rc_control(0, fb, 0, speed)

    return error


while True:

    img = drone.get_frame_read().frame

    img = cv2.resize(img, (width, height))

    img, info = find_face(img)

    previous_error = track_face(info, width, pid, previous_error)

    cv2.imshow("Output", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        drone.land()

        break
