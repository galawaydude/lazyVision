import os
import warnings
import cv2
from hand_tracker import HandTracker
from cursor_controller import CursorController

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  
warnings.filterwarnings("ignore", category=UserWarning)  

def main():
    hand_tracker = HandTracker()
    selected_finger = hand_tracker.select_finger()
    print(f"Selected finger: {['Thumb', 'Index', 'Middle', 'Ring', 'Pinky'][selected_finger]}")

    cap = cv2.VideoCapture(0)
    cursor_controller = CursorController()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        
        frame = cv2.flip(frame, 1)

        finger_tip = hand_tracker.get_finger_tip(frame)
        if finger_tip:
            
            h, w, _ = frame.shape
            cx, cy = int(finger_tip.x * w), int(finger_tip.y * h)
            cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)
            
            cursor_controller.move_cursor(finger_tip.x, finger_tip.y)

        
        cv2.putText(frame, "Press 'q' to quit", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

        
        cv2.imshow('Finger Cursor Control', frame)
        
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()