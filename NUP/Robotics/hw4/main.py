import bluetooth
import sys
import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Drawing utility
mp_drawing = mp.solutions.drawing_utils

def count_fingers(landmarks):
  # Extract fingertip landmarks
  fingertips = {
      mp_hands.HandLandmark.THUMB_TIP: landmarks[mp_hands.HandLandmark.THUMB_TIP],
      mp_hands.HandLandmark.INDEX_FINGER_TIP: landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP],
      mp_hands.HandLandmark.MIDDLE_FINGER_TIP: landmarks[mp_hands.HandLandmark.MIDDLE_FINGER_TIP],
      mp_hands.HandLandmark.RING_FINGER_TIP: landmarks[mp_hands.HandLandmark.RING_FINGER_TIP],
      mp_hands.HandLandmark.PINKY_TIP: landmarks[mp_hands.HandLandmark.PINKY_TIP]
  }

  # Count extended fingers based on y-coordinate (highest is extended)
  count = 0
  for landmark in fingertips.values():
    if landmark.y < landmarks[mp_hands.HandLandmark.WRIST].y:  # Consider below wrist as extended
      count += 1
  return count

def classify_gesture(landmarks):
    # Extract key points
    wrist = np.array([landmarks[mp_hands.HandLandmark.WRIST].x, landmarks[mp_hands.HandLandmark.WRIST].y])
    thumb_tip = np.array([landmarks[mp_hands.HandLandmark.THUMB_TIP].x, landmarks[mp_hands.HandLandmark.THUMB_TIP].y])
    index_finger_tip = np.array([landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x, landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y])
    pinky_tip = np.array([landmarks[mp_hands.HandLandmark.PINKY_TIP].x, landmarks[mp_hands.HandLandmark.PINKY_TIP].y])

    # Vectors and angles for gesture recognition
    index_to_pinky = pinky_tip - index_finger_tip
    thumb_to_wrist = wrist - thumb_tip

    # Calculate angles
    index_pinky_angle = np.arctan2(index_to_pinky[1], index_to_pinky[0]) * 180 / np.pi
    thumb_wrist_angle = np.arctan2(thumb_to_wrist[1], thumb_to_wrist[0]) * 180 / np.pi

    # Define gestures based on angles and distances
    if index_pinky_angle < -10:
        return "Right"
    elif index_pinky_angle > 10:
        return "Left"
    elif thumb_wrist_angle < -10:
        return "Forward"
    elif thumb_wrist_angle > 10:
        return "Backward"
    else:
        return "Stop"

def setup_bluetooth(device_address, device_pin):
    try:
        # Create a Bluetooth socket
        sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

        # Pair with the device (if not already paired)
        if not bluetooth.lookup_name(device_address):
            print("Pairing with device...")
            bluetooth.pair(device_address, device_pin)

        # Connect to the device
        sock.connect((device_address, 1))  # 1 is the port number, usually 1 for RFCOMM
        return sock
    except Exception as e:
        print("Error:", e)
        sys.exit(1)


def send_data_to_device(data, sock):
    try:
        sock.send(data)
    except Exception as e:
        print("Error:", e)


def forward(sock):
    send_data_to_device('0', sock)
    return


def backward(sock):
    send_data_to_device('1', sock)
    return


def right(sock):
    send_data_to_device('2', sock)
    return


def left(sock):
    send_data_to_device('3', sock)
    return


def stop(sock):
    send_data_to_device('6', sock)
    return


def main():
    device_address = "00:23:04:00:08:29"
    device_pin = 1234
    sock = setup_bluetooth(device_address, device_pin)
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # Convert image to RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        results = hands.process(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                counter = count_fingers(hand_landmarks.landmark)
                gesture = classify_gesture(hand_landmarks.landmark)
                if gesture == "Forward":
                    forward(sock)
                elif gesture == "Backward":
                    backward(sock)
                elif gesture == "Right":
                    right(sock)
                elif gesture == "Left":
                    left(sock)
                elif gesture == "Stop":
                    stop(sock)
                # Draw gesture text on the screen
                cv2.putText(image, f"Fingers: {counter}", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                cv2.putText(image, f"Gesture: {gesture}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:  # ESC to exit
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
