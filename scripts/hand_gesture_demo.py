import cv2
import mediapipe as mp
import time
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = 'data/models/gesture_recognizer.task'
DASH_DETECTION_COOLDOWN = 10

def detect_dash(show_video=False):
    cooldown = 0

    base_options = python.BaseOptions(model_asset_path=model_path)
    options = vision.GestureRecognizerOptions(
        base_options=base_options,
        running_mode=vision.RunningMode.VIDEO
    )
    recognizer = vision.GestureRecognizer.create_from_options(options)
    
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        start = time.time()
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
                print("DASH")
                cooldown = DASH_DETECTION_COOLDOWN
        
        cooldown = max(0, cooldown - 1)


        end = time.time()
        # print("Time:", (end - start) * 1000, "ms")

        if show_video:
            cv2.putText(frame, gesture_name, (30, 50), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.imshow('MediaPipe Gesture Detection', frame)
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    detect_dash(show_video=True)
