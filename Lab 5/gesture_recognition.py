import cv2
import mediapipe as mp
import time
import math

# Initialize MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)
mpDraw = mp.solutions.drawing_utils

# Hand landmark indices
# Thumb: 4 (tip), 3 (IP), 2 (MCP)
# Index: 8 (tip), 6 (PIP), 5 (MCP)
# Middle: 12 (tip), 10 (PIP), 9 (MCP)
# Ring: 16 (tip), 14 (PIP), 13 (MCP)
# Pinky: 20 (tip), 18 (PIP), 17 (MCP)
# Wrist: 0

def calculate_distance(point1, point2):
    """Calculate Euclidean distance between two points"""
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

def is_finger_extended(landmarks, finger_tip, finger_pip, finger_mcp):
    """
    Check if a finger is extended
    Returns True if finger tip is further from wrist than PIP joint
    """
    tip = landmarks[finger_tip]
    pip = landmarks[finger_pip]
    mcp = landmarks[finger_mcp]
    wrist = landmarks[0]
    
    # For thumb, check horizontal position (x coordinate for right hand)
    # Note: MediaPipe returns mirrored coordinates, so we check x
    if finger_tip == 4:  # Thumb
        # For thumb, check if tip is to the right of PIP (extended outward)
        # Also check if it's above MCP (not fully closed)
        return tip.x > pip.x and tip.y < mcp.y
    else:
        # For other fingers, check vertical position (y coordinate)
        return tip.y < pip.y  # Finger extended if tip is above PIP

def detect_gesture(landmarks):
    """
    Detect gesture based on hand landmarks
    Returns: 'good', 'bad', or 'none'
    """
    if not landmarks:
        return 'none'
    
    # Check each finger state
    thumb_extended = is_finger_extended(landmarks, 4, 3, 2)
    index_extended = is_finger_extended(landmarks, 8, 6, 5)
    middle_extended = is_finger_extended(landmarks, 12, 10, 9)
    ring_extended = is_finger_extended(landmarks, 16, 14, 13)
    pinky_extended = is_finger_extended(landmarks, 20, 18, 17)
    
    # Get thumb tip and wrist positions for thumbs up/down detection
    thumb_tip = landmarks[4]
    thumb_ip = landmarks[3]
    wrist = landmarks[0]
    
    # Thumbs Up (Good gesture)
    # Thumb extended upward (tip y < IP y) and other fingers closed
    if (thumb_extended and 
        thumb_tip.y < thumb_ip.y and  # Thumb pointing up
        not index_extended and 
        not middle_extended and 
        not ring_extended and 
        not pinky_extended):
        return 'good'
    
    # Thumbs Down (Bad gesture)
    # Thumb extended downward (tip y > IP y) and other fingers closed
    if (thumb_extended and 
        thumb_tip.y > thumb_ip.y and  # Thumb pointing down
        not index_extended and 
        not middle_extended and 
        not ring_extended and 
        not pinky_extended):
        return 'bad'
    
    # Closed Fist (Bad gesture)
    # All fingers closed
    if (not thumb_extended and 
        not index_extended and 
        not middle_extended and 
        not ring_extended and 
        not pinky_extended):
        return 'bad'
    
    # OK Sign (Good gesture)
    # Thumb and index finger form a circle, other fingers extended
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    thumb_ip = landmarks[3]
    index_pip = landmarks[6]
    
    # Check if thumb and index tips are close (forming a circle)
    distance_ok = calculate_distance(thumb_tip, index_tip)
    # Threshold for OK sign (normalized coordinates, adjust as needed)
    if (distance_ok < 0.05 and 
        thumb_tip.y < thumb_ip.y and  # Thumb up
        index_tip.y < index_pip.y and  # Index up
        middle_extended and 
        ring_extended and 
        pinky_extended):
        return 'good'
    
    # Open palm with all fingers extended (Good gesture)
    if (thumb_extended and 
        index_extended and 
        middle_extended and 
        ring_extended and 
        pinky_extended):
        return 'good'
    
    return 'none'

def main():
    # Camera settings
    wCam, hCam = 640, 480
    
    cap = cv2.VideoCapture(0)
    cap.set(3, wCam)
    cap.set(4, hCam)
    
    pTime = 0
    gesture_state = 'none'
    gesture_frames = 0  # Count consecutive frames with same gesture
    min_frames = 5  # Minimum frames to confirm gesture
    
    print("Gesture Recognition Started!")
    print("Show a gesture to the camera:")
    print("- Thumbs Up = GOOD")
    print("- Thumbs Down = BAD")
    print("- Closed Fist = BAD")
    print("- Open Palm = GOOD")
    print("- Press 'q' to quit")
    
    while True:
        success, img = cap.read()
        if not success:
            break
        
        # Flip image horizontally for mirror effect
        img = cv2.flip(img, 1)
        
        # Convert BGR to RGB
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        
        current_gesture = 'none'
        
        # Draw hand landmarks and detect gesture
        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                # Draw landmarks
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                
                # Detect gesture
                current_gesture = detect_gesture(handLms.landmark)
        
        # Update gesture state with frame counting for stability
        if current_gesture == gesture_state:
            gesture_frames += 1
        else:
            gesture_frames = 1
            gesture_state = current_gesture
        
        # Only display gesture if detected for minimum frames
        if gesture_frames >= min_frames:
            if gesture_state == 'good':
                # Draw a green rectangle background
                cv2.rectangle(img, (40, 40), (300, 140), (0, 255, 0), -1)
                # Display "GOOD!" in black text on green background
                cv2.putText(img, 'GOOD!', (50, 100), 
                           cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 0), 4)
            elif gesture_state == 'bad':
                # Draw a red rectangle background
                cv2.rectangle(img, (40, 40), (250, 140), (0, 0, 255), -1)
                # Display "BAD!" in white text on red background
                cv2.putText(img, 'BAD!', (50, 100), 
                           cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 4)
        
        # Calculate and display FPS
        cTime = time.time()
        fps = 1 / (cTime - pTime) if (cTime - pTime) > 0 else 0
        pTime = cTime
        
        cv2.putText(img, f'FPS: {int(fps)}', (10, 30), 
                   cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
        
        # Display current gesture status (for debugging)
        cv2.putText(img, f'Gesture: {gesture_state.upper()}', (10, hCam - 20), 
                   cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)
        
        cv2.imshow("Gesture Recognition", img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    hands.close()

if __name__ == "__main__":
    main()
