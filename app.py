import cv2
import time
import math
import numpy as np
import streamlit as st
import HandTrackingModule as htm
from pycaw.pycaw import AudioUtilities

st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox(
    "Choose the Application", ["Finger Counting", "Gesture Volume Control"]
)

st.title(app_mode)
run = st.checkbox("Run Webcam")
stframe = st.empty()

wCam, hCam = 640, 480

if run:
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)

    pTime = 0

    if app_mode == "Finger Counting":
        detector = htm.handDetector(detectionCon=0.75)
        tipIds = [4, 8, 12, 16, 20]

        while run:
            success, img = cap.read()
            if not success:
                st.error("Failed to access webcam.")
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
                img,
                f"FPS: {int(fps)}",
                (10, 70),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (255, 0, 255),
                3,
            )

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            stframe.image(img_rgb, channels="RGB")

    elif app_mode == "Gesture Volume Control":
        detector = htm.handDetector(detectionCon=0.7)

        device = AudioUtilities.GetSpeakers()
        volume = device.EndpointVolume
        volRange = volume.GetVolumeRange()
        minVol = volRange[0]
        maxVol = volRange[1]
        vol = 0
        volBar = 400
        volPer = 0

        while run:
            success, img = cap.read()
            if not success:
                st.error("Failed to access webcam.")
                break

            img = detector.findHands(img)
            lmList = detector.findPosition(img, draw=False)

            if len(lmList) != 0:
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

                length = math.hypot(x2 - x1, y2 - y1)

                vol = np.interp(length, [50, 150], [minVol, maxVol])
                volBar = np.interp(length, [50, 150], [400, 150])
                volPer = np.interp(length, [50, 150], [0, 100])

                volume.SetMasterVolumeLevel(vol, None)

                if length < 50:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

            cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
            cv2.rectangle(img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED)

            cTime = time.time()
            fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
            pTime = cTime

            cv2.putText(
                img,
                f"FPS: {int(fps)}",
                (100, 70),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (255, 0, 0),
                3,
            )
            cv2.putText(
                img,
                f"{int(volPer)} %",
                (40, 450),
                cv2.FONT_HERSHEY_PLAIN,
                3,
                (0, 255, 0),
                3,
            )

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            stframe.image(img_rgb, channels="RGB")

    cap.release()
