import streamlit as st
import cv2
import math
import numpy as np
import HandTrackingModule as htm
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import av

st.sidebar.title("Navigation")
app_mode = st.sidebar.selectbox(
    "Choose the Application", ["Finger Counting", "Gesture Volume Control"]
)
st.title(app_mode)


class VideoProcessor(VideoTransformerBase):
    def __init__(self):
        self.tipIds = [4, 8, 12, 16, 20]
        # FIX: Initialize the detector directly inside the WebRTC thread
        self.detector = htm.handDetector(detectionCon=0.7)

    def recv(self, frame):
        # Convert frame from WebRTC to OpenCV format
        img = frame.to_ndarray(format="bgr24")

        # Process the image using the thread-safe detector
        img = self.detector.findHands(img)
        lmList = self.detector.findPosition(img, draw=False)

        if len(lmList) != 0:
            if app_mode == "Finger Counting":
                fingers = []
                # Thumb
                if lmList[self.tipIds[0]][1] < lmList[self.tipIds[0] - 1][1]:
                    fingers.append(0)
                else:
                    fingers.append(1)

                # 4 Fingers
                for id in range(1, 5):
                    if lmList[self.tipIds[id]][2] < lmList[self.tipIds[id] - 2][2]:
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

            elif app_mode == "Gesture Volume Control":
                x1, y1 = lmList[4][1], lmList[4][2]
                x2, y2 = lmList[8][1], lmList[8][2]
                cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

                cv2.circle(img, (x1, y1), 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (x2, y2), 10, (255, 0, 0), cv2.FILLED)
                cv2.circle(img, (cx, cy), 10, (255, 0, 0), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

                length = math.hypot(x2 - x1, y2 - y1)

                # Visual Math calculations
                volBar = np.interp(length, [50, 150], [400, 150])
                volPer = np.interp(length, [50, 150], [0, 100])

                if length < 50:
                    cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

                cv2.rectangle(img, (50, 150), (85, 400), (0, 255, 0), 3)
                cv2.rectangle(
                    img, (50, int(volBar)), (85, 400), (0, 255, 0), cv2.FILLED
                )
                cv2.putText(
                    img,
                    f"Vol Demo: {int(volPer)} %",
                    (40, 450),
                    cv2.FONT_HERSHEY_PLAIN,
                    3,
                    (0, 255, 0),
                    3,
                )

        # Return the processed frame to the browser
        return av.VideoFrame.from_ndarray(img, format="bgr24")


# Create a WebRTC config using Google's free STUN server to bypass firewalls
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# Start the WebRTC stream with the config and disable audio
webrtc_streamer(
    key="example",
    video_processor_factory=VideoProcessor,
    rtc_configuration=RTC_CONFIGURATION,
    media_stream_constraints={"video": True, "audio": False},
)
