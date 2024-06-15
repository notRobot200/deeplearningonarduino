import cv2
import mediapipe as mp
import controller

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(static_image_mode=False,
                       max_num_hands=1,
                       min_detection_confidence=0.5,
                       min_tracking_confidence=0.5)


# Function to classify gestures
def classify_hand_gesture(landmarks):
    thumb_mcp = landmarks[2]
    thumb_tip = landmarks[4]
    index_finger_pip = landmarks[6]
    index_finger_tip = landmarks[8]
    middle_finger_pip = landmarks[10]
    middle_finger_tip = landmarks[12]
    ring_finger_pip = landmarks[14]
    ring_finger_tip = landmarks[16]
    pinky_pip = landmarks[18]
    pinky_tip = landmarks[20]

    # print("Index finger tip y:", index_finger_tip.y)
    # print("Index finger pip y:", index_finger_pip.y)
    # print("Middle finger tip y:", middle_finger_tip.y)
    # print("Middle finger pip y:", middle_finger_pip.y)
    # print("Ring finger tip y:", ring_finger_tip.y)
    # print("Ring finger pip y:", ring_finger_pip.y)
    # print("Pinky tip y:", pinky_tip.y)
    # print("Pinky pip y:", pinky_pip.y)

    if index_finger_tip.y < index_finger_pip.y and middle_finger_tip.y < middle_finger_pip.y and ring_finger_tip.y < ring_finger_pip.y and pinky_tip.y < pinky_pip.y:
        return "paper"

    elif index_finger_tip.y > index_finger_pip.y and middle_finger_tip.y > middle_finger_pip.y and ring_finger_tip.y > ring_finger_pip.y and pinky_tip.y > pinky_pip.y:
        return "rock"

    elif index_finger_tip.y < index_finger_pip.y and middle_finger_tip.y < middle_finger_pip.y and ring_finger_tip.y > ring_finger_pip.y and pinky_tip.y > pinky_pip.y:
        return "scissors"

    elif thumb_tip.y < thumb_mcp.y and index_finger_tip.y > index_finger_pip.y and middle_finger_tip.y > middle_finger_pip.y and ring_finger_tip.y > ring_finger_pip.y and pinky_tip.y < pinky_pip.y:
        return "off"

    else:
        return "none"

cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Tidak dapat mengakses frame kamera.")
        continue

    # RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process images using MediaPipe Hands
    results = hands.process(image_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Take a hand landmark position
            landmarks = hand_landmarks.landmark
            gesture = classify_hand_gesture(landmarks)

            # Show detected gestures
            cv2.putText(image, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            # Send gesture to controller.py
            controller.led(gesture)
    else:
        # If no hand is detected, send 'nohand' to controller.py
        controller.led('nohand')

    cv2.imshow('Hand Gesture Detection', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

# Turns off all LEDs when the program is stopped
controller.turn_off()
cap.release()
cv2.destroyAllWindows()
