# 🖐️ Real-Time Hand Tracking & Gesture Control System

[![Python](https://img.shields.io/badge/Python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-5C3EE8.svg?logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-Hand%20Landmarks-00C4B4.svg?logo=google&logoColor=white)](https://developers.google.com/mediapipe)
[![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B.svg?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Streamlit-WebRTC](https://img.shields.io/badge/WebRTC-In--Browser%20Streaming-orange.svg)](https://github.com/whitphx/streamlit-webrtc)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An interactive, high-performance Computer Vision system utilizing **Google MediaPipe** and **OpenCV** to perform 21-point 3D hand landmark tracking. The repository features modular gesture detection, a real-time finger counter, dynamic system volume control via hand gestures, and multi-environment Streamlit web applications (including WebRTC cloud streaming).

---

## 📌 Table of Contents

- [Features](#-features)
- [How It Works](#-how-it-works)
  - [Hand Landmark Topology](#hand-landmark-topology)
  - [Gesture Algorithms](#gesture-algorithms)
- [Project Architecture](#-project-architecture)
- [Prerequisites & Requirements](#-prerequisites--requirements)
- [Installation & Setup](#-installation--setup)
- [Running the Applications](#-running-the-applications)
  - [1. Standalone Core Modules](#1-standalone-core-modules)
  - [2. Local Desktop Streamlit App (`app.py`)](#2-local-desktop-streamlit-app-apppy)
  - [3. Cross-Platform Simulation App (`app1.py`)](#3-cross-platform-simulation-app-app1py)
  - [4. Cloud WebRTC Streamlit App (`app2.py`)](#4-cloud-webrtc-streamlit-app-app2py)
- [Cloud Deployment Notes](#-cloud-deployment-notes)
- [Technologies Used](#-technologies-used)
- [Contributing](#-contributing)
- [Author](#-author)

---

## ✨ Features

- **High-Precision 21-Point Hand Landmark Detection:** Built on top of Google MediaPipe Hands ML pipeline for sub-millisecond, low-latency landmark tracking.
- **Modular OOP Hand Tracking Module (`HandTrackingModule.py`):** Encapsulated, reusable detector class (`handDetector`) that can easily integrate into any downstream vision application.
- **Real-Time Finger Counting:** Accurately counts raised fingers (0 to 5) with visual digit overlay and real-time FPS counter.
- **Hand Gesture System Volume Control:**
  - Calculates Euclidean distance between the thumb and index finger tips.
  - Dynamically adjusts the Windows master audio volume level in real time using `pycaw`.
  - Provides intuitive on-screen visual feedback (custom volume bar, percentage text, and target indicator).
- **Multi-Modal Streamlit Applications:**
  - **`app.py`:** Local desktop application with sidebar navigation and direct Windows audio driver integration.
  - **`app1.py`:** Standalone visual simulation mode (platform-agnostic, safe for macOS / Linux where PyCAW Windows APIs are unavailable).
  - **`app2.py`:** Cloud-ready WebRTC application using `streamlit-webrtc` and Google STUN servers to stream client-side webcam video directly through the browser.

---

## 🧠 How It Works

### Hand Landmark Topology

The system maps each detected hand to **21 3D landmarks** with $(x, y, z)$ coordinates:

```
    8   12  16  20      Landmark IDs:
    |   |   |   |       • 0: Wrist
    7   11  15  19      • 1-4: Thumb (4 = Tip)
    |   |   |   |       • 5-8: Index Finger (8 = Tip)
4   6   10  14  18      • 9-12: Middle Finger (12 = Tip)
 \  |   |   |   |       • 13-16: Ring Finger (16 = Tip)
  3 5---9---13--17      • 17-20: Pinky Finger (20 = Tip)
   \|           |
    2           |
     \         /
      1       /
       \     /
          0
```

### Gesture Algorithms

1. **Finger Counting Logic:**
   - **Four Fingers (Index, Middle, Ring, Pinky):** Evaluates if the tip landmark $y$-coordinate is higher up on screen (lower numerical pixel value) than its corresponding PIP (Proximal Interphalangeal) joint:
     $$\text{Finger Up} \iff y_{\text{tip}} < y_{\text{pip}}$$
   - **Thumb:** Compares the $x$-coordinate of the thumb tip relative to the thumb IP joint.
   - Aggregates the total count ($0 - 5$) and renders the count overlay.

2. **Volume Control Mapping:**
   - Detects Landmark 4 (Thumb Tip) and Landmark 8 (Index Tip).
   - Computes the Euclidean distance:
     $$d = \sqrt{(x_2 - x_1)^2 + (y_2 - y_1)^2}$$
   - Maps $d$ (calibrated between $[50, 150]$ pixels) using `numpy.interp` to:
     - Master Volume dB level ($[\text{minVol}, \text{maxVol}]$ via PyCAW)
     - On-screen volume bar height ($[400\text{px}, 150\text{px}]$)
     - Volume percentage ($[0\%, 100\%]$)

---

## 📂 Project Architecture

```plaintext
Hand-Tracking-Project/
├── HandTrackingModule.py      # Core OOP wrapper for MediaPipe Hands
├── FingerCountingProject.py   # Standalone Streamlit finger counting script
├── VolumeHandControl.py       # Standalone Streamlit gesture volume control script
├── app.py                     # Unified Streamlit app (Finger Counter + PyCAW Volume Control)
├── app1.py                    # Unified Streamlit app (Cross-platform visual simulation)
├── app2.py                    # Cloud-ready Streamlit app using WebRTC for in-browser webcam
├── packages.txt               # Debian/Ubuntu dependencies for Streamlit Cloud deployment
├── requirements.txt           # Python package dependencies
├── .gitignore                 # Standard Python & virtualenv ignores
└── README.md                  # Project documentation
```

---

## ⚙️ Prerequisites & Requirements

- **Operating System:**
  - Windows 10/11 (fully supports `pycaw` audio control in `app.py` and `VolumeHandControl.py`)
  - Linux / macOS (supported using `app1.py` or `app2.py`)
- **Python:** Version `3.8` to `3.11` recommended
- **Hardware:** Standard USB or integrated webcam

---

## 🚀 Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/ankitdas2124/Hand-Tracking-Projects.git
   cd Hand-Tracking-Projects
   ```

2. **Create and Activate a Virtual Environment:**
   - **Windows (Command Prompt / PowerShell):**
     ```powershell
     python -m venv .venv
     .venv\Scripts\activate
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## 🖥️ Running the Applications

### 1. Standalone Core Modules

- **Test Hand Tracking Module directly via OpenCV window:**
  ```bash
  python HandTrackingModule.py
  ```
  *(Press `Esc` to exit the OpenCV window)*

- **Run standalone Finger Counting Streamlit page:**
  ```bash
  streamlit run FingerCountingProject.py
  ```

- **Run standalone Volume Control Streamlit page:**
  ```bash
  streamlit run VolumeHandControl.py
  ```

### 2. Local Desktop Streamlit App (`app.py`)
Provides a unified navigation sidebar to switch between **Finger Counting** and **Gesture Volume Control** with real-time Windows master audio control:
```bash
streamlit run app.py
```

### 3. Cross-Platform Simulation App (`app1.py`)
Simulates volume changes visually without binding to Windows-specific audio libraries (ideal for Linux, macOS, or presentations):
```bash
streamlit run app1.py
```

### 4. Cloud WebRTC Streamlit App (`app2.py`)
Designed for deployed web servers (such as Streamlit Community Cloud) where the server has no local webcam. It streams the user's browser webcam directly to the processing loop using WebRTC:
```bash
streamlit run app2.py
```

---

## ☁️ Cloud Deployment Notes

When deploying on **Streamlit Community Cloud** or Linux Docker containers:
1. **Server Webcam Limitation:** Deployed cloud servers cannot open `cv2.VideoCapture(0)` because the server has no attached physical camera. **Use `app2.py` as your main entrypoint** for cloud deployments.
2. **Linux System Libraries:** The included `packages.txt` ensures that required OpenCV / OpenGL graphical libraries are automatically provisioned by the host container:
   - `freeglut3-dev`
   - `libgtk2.0-dev`
   - `libgl1-mesa-glx`
3. **Audio Handling:** Use `app1.py` (visual simulator) or `app2.py` (WebRTC) in cloud environments as `pycaw` requires the Windows Core Audio API.

---

## 🛠️ Technologies Used

| Library / Tool | Purpose |
| :--- | :--- |
| **Python** | Core programming language |
| **OpenCV (`opencv-python-headless`)** | Video stream capture, image preprocessing, and graphics drawing |
| **MediaPipe** | ML-based real-time 3D hand tracking and landmark estimation |
| **Streamlit** | Rapid, interactive web application framework |
| **Streamlit-WebRTC** | Real-time audio/video streaming via WebRTC in Streamlit |
| **PyCAW** | Python Core Audio Windows Library for system volume control |
| **NumPy** | High-performance numerical operations and interpolation |

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 👤 Author

- **Ankit Das** - [GitHub Profile](https://github.com/ankitdas2124)
- Repository: [Hand-Tracking-Projects](https://github.com/ankitdas2124/Hand-Tracking-Projects)
