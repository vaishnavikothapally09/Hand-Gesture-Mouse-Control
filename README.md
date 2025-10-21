# Hand-Gesture-Mouse-Control

This is a real-time project that allows users to control the mouse cursor using hand gestures, powered by computer vision and AI. It uses **OpenCV**, **MediaPipe**, and **PyAutoGUI** to interpret hand movements and translate them into mouse actions like move, click, drag, scroll, and volume control.

## Features

- Move mouse with index finger
- Left click with index + middle finger tap
- Right click with index + middle finger hold
- Double click with rapid two-finger tap
- Scroll up/down with vertical finger movement
- Drag and drop by pinch and hold gesture
- Volume control using finger distance

## Technologies Used

- Python
- OpenCV
- MediaPipe
- PyAutoGUI
- NumPy
- pynput (for additional mouse control)
- Custom utility module (`util.py`) for angle and distance calculations

## Installation

Make sure Python is installed on your system. Then install the required libraries:

```bash
pip install opencv-python mediapipe pyautogui pynput numpy
```

## How to Run

1. Download the project files.
2. Run the main Python script:

```bash
python main.py
```

3. Show your hand in front of the webcam and start controlling the mouse using gestures.

> Ensure your camera is working properly. Use a well-lit environment for better gesture recognition.

You can also run the project using **Anaconda (Spyder)** or **VS Code**:
- Open the project folder in Spyder or VS Code.
- Set the correct working directory.
- Run `main.py` from the editor.

## Project Structure

```
hand-gesture-mouse-control/
├── main.py
├── util.py
├── README.md
└── requirements.txt
```
