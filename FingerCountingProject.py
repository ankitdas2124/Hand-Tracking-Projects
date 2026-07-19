import cv2
import time
import streamlit as st
import HandTrackingModule as htm

st.title("Live Finger Counter")
run = st.checkbox("Run Webcam")
stframe = st.empty()

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0
detector = htm.handDetector(detectionCon=0.75)
tipIds = [4, 8, 12, 16, 20]

while run:
    success, img = cap.read()
    if not success:
        break

    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)

    if len(lmList) != 0:
        fingers = []

        if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
            fingers.append(0)
        else:
            fingers.append(1)

        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)

        cv2.rectangle(img, (20, 255), (170, 425), (0, 255, 0), cv2.FILLED)
        cv2.putText(
            img,
            str(totalFingers),
            (45, 390),
            cv2.FONT_HERSHEY_PLAIN,
            10,
            (255, 0, 0),
            25,
        )

    cTime = time.time()
    fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
    pTime = cTime

    cv2.putText(
        img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3
    )

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    stframe.image(img_rgb, channels="RGB")

cap.release()
