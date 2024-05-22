from handDetector import HandDetector
import cv2
import math
import numpy as np
# import bluetooth
import sys


handDetector = HandDetector(min_detection_confidence=0.7)
webcamFeed = cv2.VideoCapture(0)


def setup_bluetooth(device_address, device_pin):
    try:
        # Create a Bluetooth socket
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        # Pair with the device (if not already paired)
        if not bluetooth.lookup_name(device_address):
            print("Pairing with device...")
            bluetooth.pair(device_address, device_pin)

        # Connect to the device
        sock.connect((device_address, 1))  # 1 is the port number, usually 1 for RFCOMM
        return sock
    except Exception as e:
        print("Error:", e)
        sys.exit(1)


def send_data_to_device(data, sock):
    try:
        sock.send(data)
    except Exception as e:
        print("Error:", e)


def forward(sock):
    send_data_to_device('0', sock)
    return


def backward(sock):
    send_data_to_device('1', sock)
    return


def right(sock):
    send_data_to_device('2', sock)
    return


def left(sock):
    send_data_to_device('3', sock)
    return


def stop(sock):
    send_data_to_device('6', sock)
    return



# device_address = "00:23:04:00:08:29"
# device_pin = 1234
# sock = setup_bluetooth(device_address, device_pin)


while True:
    status, image = webcamFeed.read()
    handLandmarks = handDetector.findHandLandMarks(image=image, draw=True)
    count=0

    if(len(handLandmarks) != 0):
        #we will get y coordinate of finger-tip and check if it lies above middle landmark of that finger
        #details: https://google.github.io/mediapipe/solutions/hands

        if handLandmarks[4][3] == "Right" and handLandmarks[4][1] > handLandmarks[3][1]:       #Right Thumb
            count = count+1
        elif handLandmarks[4][3] == "Left" and handLandmarks[4][1] < handLandmarks[3][1]:       #Left Thumb
            count = count+1
        if handLandmarks[8][2] < handLandmarks[6][2]:       #Index finger
            count = count+1
        if handLandmarks[12][2] < handLandmarks[10][2]:     #Middle finger
            count = count+1
        if handLandmarks[16][2] < handLandmarks[14][2]:     #Ring finger
            count = count+1
        if handLandmarks[20][2] < handLandmarks[18][2]:     #Little finger
            count = count+1

    # if count == 0:
    #     stop(sock)
    # elif count == 1:
    #     forward(sock)
    # elif count == 2:
    #     backward(sock)
    # elif count == 3:
    #     right(sock)
    # elif count == 4:
    #     left(sock)
    # else:
    #     stop(sock)

    cv2.putText(image, str(count), (45, 375), cv2.FONT_HERSHEY_SIMPLEX, 5, (255, 0, 0), 25)
    cv2.imshow("Volume", image)
    cv2.waitKey(1)
