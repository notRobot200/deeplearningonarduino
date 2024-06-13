import cv2
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model

# Memuat model
model = load_model('rock_paper_scissors_cnn.h5')

# Definisi label
labels = ['Rock', 'Paper', 'Scissors']


# Fungsi untuk melakukan prediksi
def predict(frame):
    img = cv2.resize(frame, (150, 150))  # Ubah ukuran sesuai dengan input model
    img = np.expand_dims(img, axis=0)
    img = img / 255.0  # Normalisasi gambar
    predictions = model.predict(img)
    return labels[np.argmax(predictions)]


# Menggunakan webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Error: Failed to capture image")
        break

    # Membalikkan frame horizontal (opsional)
    frame = cv2.flip(frame, 1)

    # Membuat persegi untuk area prediksi (lebih besar)
    start_point = (50, 50)
    end_point = (450, 450)
    color = (255, 0, 0)
    thickness = 2
    cv2.rectangle(frame, start_point, end_point, color, thickness)

    # Memotong area persegi untuk prediksi (lebih besar)
    roi = frame[50:450, 50:450]

    # Melakukan prediksi
    prediction = predict(roi)

    # Menampilkan hasil prediksi di layar
    cv2.putText(frame, prediction, (100, 90), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Menampilkan frame
    cv2.imshow('Rock Paper Scissors Prediction', frame)

    # Keluar jika menekan tombol 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Melepaskan webcam dan menutup jendela
cap.release()
cv2.destroyAllWindows()
