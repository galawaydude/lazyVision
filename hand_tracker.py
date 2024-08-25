import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.5
        )
        self.selected_finger = None

    def select_finger(self):
        cap = cv2.VideoCapture(0)
        while True:
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb_frame)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                
                cv2.putText(frame, "Point with the finger you want to use", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(frame, "Press 'S' to select", (10, 60), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                
                cv2.imshow("Select Finger", frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('s'):
                    
                    finger_tips = [hand_landmarks.landmark[i] for i in [4, 8, 12, 16, 20]]
                    self.selected_finger = finger_tips.index(min(finger_tips, key=lambda p: p.y))
                    break

        cap.release()
        cv2.destroyAllWindows()
        return self.selected_finger

    def get_finger_tip(self, frame):
        if self.selected_finger is None:
            return None

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            return hand_landmarks.landmark[self.selected_finger * 4 + 4]  # Tip landmarks are at 4, 8, 12, 16, 20
        return None