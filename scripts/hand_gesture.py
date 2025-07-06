import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from pynput.keyboard import Key, Controller
import time

model_path = 'data/models/gesture_recognizer.task'
DASH_DETECTION_COOLDOWN = 10

def detect_dash():
    cooldown = 0
    keyboard = Controller()

    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.GestureRecognizerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO
    )
    recognizer = vision.GestureRecognizer.create_from_options(options)
    
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)

        timestamp = int(time.time() * 1000)
        recognition_result = recognizer.recognize_for_video(mp_image, timestamp)

        gesture_name = "No Hand Detected"
        if recognition_result.gestures and recognition_result.gestures[0]:
            top_gesture = recognition_result.gestures[0][0]
            gesture_name = top_gesture.category_name
            if gesture_name == 'Open_Palm' and cooldown == 0:
                keyboard.type('x')
                cooldown = DASH_DETECTION_COOLDOWN
        
        cooldown = max(0, cooldown - 1)

    if cap is not None:
        cap.release()
