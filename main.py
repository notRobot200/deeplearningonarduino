import cv2
import controller as cnt
import tensorflow as tf
import numpy as np

# Load the trained model
model = tf.keras.models.load_model('rock_paper_scissors_cnn.h5')


# Preprocess the frame for prediction
def preprocess_frame(frame):
    frame = cv2.resize(frame, (150, 150))
    frame = frame / 255.0
    frame = np.expand_dims(frame, axis=0)
    return frame


# Gesture labels
gesture_labels = ['rock', 'paper', 'scissor']

video = cv2.VideoCapture(0)

while True:
    ret, frame = video.read()
    frame = cv2.flip(frame, 1)

    # Preprocess the frame and predict gesture
    processed_frame = preprocess_frame(frame)
    predictions = model.predict(processed_frame)
    gesture_index = np.argmax(predictions)
    gesture = gesture_labels[gesture_index]

    cnt.led(gesture)

    cv2.putText(frame, f'Gesture: {gesture}', (20, 460), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1, cv2.LINE_AA)

    cv2.imshow("frame", frame)
    k = cv2.waitKey(1)
    if k == ord("k"):
        break

video.release()
cv2.destroyAllWindows()
