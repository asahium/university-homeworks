import cv2
import time
import os
import HandTrackingModule as htm

wCam, hCam = 300, 400

cap = cv2.VideoCapture('countFingers.mp4')
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

detector = htm.handDetector(detectionCon=1)

tipIds = [4, 8, 12, 16, 20]
sum = 0

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    landmarks_list = detector.findPosition(img, draw=False)

    if len(landmarks_list) != 0:
        fingers_list = []

        #Check for thumb
        if landmarks_list[tipIds[0]][1] > landmarks_list[tipIds[0] - 1][1]:
            fingers_list.append(1)
        else:
            fingers_list.append(0)

        #Check for 4 fingers
        for id in range(1, 5):
            if landmarks_list[tipIds[id]][2] < landmarks_list[tipIds[id] - 2][2]:
                fingers_list.append(1)
            else:
                fingers_list.append(0)

        #print sum
        fingers_count = fingers_list.count(1)
        sum = sum + fingers_count
        print(sum)

        #display count inside the frame
        cv2.rectangle(img, (20, 225), (170, 425), (169, 169, 169), cv2.FILLED)
        cv2.putText(img, str(fingers_count), (60, 375), cv2.FONT_HERSHEY_PLAIN,
                    8, (0, 0, 128), 20)

    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    #display FPS inside the frame
    cv2.putText(img, f'Frames per second =: {int(fps)}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 0, 128), 3)

    cv2.imshow("Image", img)

    if cv2.waitKey(1) == 13:
        break

    cv2.waitKey(1)
