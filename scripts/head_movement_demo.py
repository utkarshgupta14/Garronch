import cv2
import mediapipe as mp
import time

def get_direction(show_video=False):
    # Setup
    mp_face_detection = mp.solutions.face_detection
    mp_drawing = mp.solutions.drawing_utils
    mp_detection = mp.solutions.face_detection
    prev_nose_y = None
    jump_cooldown = 0

    # Initialize face detector
    with mp_face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5) as face_detection:
        cap = cv2.VideoCapture(0)

        while cap.isOpened():
            start = time.time()
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

                    # right/ left tilt detection
                    if right_eye.y == left_eye.y:
                        print("VERTICAL FACE BRUHH")
                        continue
                    slope = (right_eye.y-left_eye.y) / (right_eye.x-left_eye.x)
                    
                    if show_video == True:
                        if slope > 0.25:
                            cv2.putText(frame, "LEFT TILT!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (0, 0, 255), 2, cv2.LINE_AA)
                        elif slope < -0.25:
                            cv2.putText(frame, "RIGHT TILT!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (0, 0, 255), 2, cv2.LINE_AA)
                        else:
                            cv2.putText(frame, "NEUTRAL!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (0, 0, 255), 2, cv2.LINE_AA)
                        mp_drawing.draw_detection(frame, detection)
                    
                    if prev_nose_y is not None:
                        if(prev_nose_y - current_nose_y > 0.02):
                            jump_cooldown = 15
                    prev_nose_y = current_nose_y
                    if jump_cooldown > 0:
                        cv2.putText(frame, "Upward Jerk Detected!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                                    1, (0, 0, 255), 2, cv2.LINE_AA)
                    jump_cooldown = max(0, jump_cooldown-1)
            
            end = time.time()
            print("Time:" , (end-start)*1000)

            if show_video:
                cv2.imshow('MediaPipe Face Detection', frame)
                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break

        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    get_direction(True)