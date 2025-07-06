import cv2
import mediapipe as mp
from pynput.keyboard import Key, Controller

def detect_head():
    # Setup
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils
    mp_detection = mp.solutions.face_detection

    right = False
    left = False
    prev_nose_y = None
    jump_cooldown = 0

    keyboard = Controller()

    cap = cv2.VideoCapture(0)

    # Initialize face detector
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        while cap.isOpened():
            success, frame = cap.read()
            if not success:
                break

            # Convert to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(image)

            # Draw detections
            if results.detections:
                for detection in results.detections:
                    left_eye = mp_detection.get_key_point(detection, mp_detection.FaceKeyPoint.LEFT_EYE)
                    right_eye = mp_detection.get_key_point(detection, mp_detection.FaceKeyPoint.RIGHT_EYE)
                    nose_tip = mp_detection.get_key_point(detection, mp_detection.FaceKeyPoint.NOSE_TIP)
                    current_nose_y = nose_tip.y

                    if right_eye.y == left_eye.y:
                        keyboard.press
                    slope = (right_eye.y-left_eye.y) / (right_eye.x-left_eye.x)
                    if slope > 0.25:
                        right = False
                        left = True
                        keyboard.press(Key.left) # left
                    elif slope < -0.25:
                        left = False
                        right = True
                        keyboard.press(Key.right) # right
                    else:
                        if right:
                            keyboard.release(Key.right)
                        elif left:
                            keyboard.release(Key.left)

                    if prev_nose_y is not None and jump_cooldown==0:
                        if(prev_nose_y - current_nose_y > 0.02):
                            jump_cooldown = 5
                            keyboard.press(Key.up)
                            keyboard.release(Key.up)
                    prev_nose_y = current_nose_y
                    jump_cooldown = max(0, jump_cooldown-1)
    if cap is not None:
        cap.release()