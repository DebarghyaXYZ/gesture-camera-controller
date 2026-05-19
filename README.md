# 📸 Gesture Controlled Smart Camera using Python & OpenCV

A real-time AI-powered smart camera system that allows users to control image capture and zoom using hand gestures.

Built using Python, OpenCV, MediaPipe, and CustomTkinter, this project combines Computer Vision, Gesture Recognition, and a Modern Desktop UI to create a touchless smart camera experience.

---

# 🚀 Features

✅ Real-Time Hand Tracking  
✅ Gesture-Based Image Capture  
✅ Smooth Zoom Control  
✅ Countdown Before Capture  
✅ Capture Cooldown Protection  
✅ Pro Mode Gesture System  
✅ Manual Capture Button  
✅ Modern CustomTkinter UI  
✅ Automatic Image Saving  
✅ Real-Time Camera Processing  

---

# 🖼️ Demo

## Main UI
(Add Screenshot Here)

## Zoom Mode
(Add Screenshot Here)

## Capture Mode
(Add Screenshot Here)

## Pro Mode
(Add Screenshot Here)

---

# 🧠 How It Works

The system detects hand landmarks using MediaPipe and processes different finger patterns to trigger camera actions.

### Supported Gestures

| Gesture | Action |
|---|---|
| Open → Close → Open | Capture Image |
| Pinch Gesture | Enable Zoom |
| Finger Distance Change | Zoom In / Out |
| Two-Hand Pro Gesture | Enable Pro Mode |
| Special Gesture | Disable Pro Mode |

---

# 🛠️ Technologies Used

- Python
- OpenCV
- MediaPipe
- CustomTkinter
- Computer Vision
- Hand Tracking
- Gesture Recognition

---

# 📂 Project Structure

```bash
Gesture-Controlled-Camera/
│
├── main.py
├── HandTrackingModule.py
├── Captured Image/
├── Essential Data/
│   └── Image Number.txt
└── README.md
