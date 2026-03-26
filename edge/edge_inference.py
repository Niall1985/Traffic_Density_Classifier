import cv2
import requests
import time
import tensorflow as tf
import numpy as np

interpreter = tf.lite.Interpreter(model_path="traffic_density_model.tflite")
interpreter.allocate_tensors()

def predict(frame):
    frame = cv2.resize(frame,(128, 128))
    frame = frame/255.0
    frame = np.expand_dims(frame, axis=0)
    frame = frame.astype(np.float32)

    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    interpreter.set_tensor(input_details[0]['index'], frame)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])

    return output.argmax()


video = cv2.VideoCapture("traffic.mp4")

frame_id = 0

while True:
    if frame_id == 30:
        break
    else:

        ret, frame = video.read()
        if not ret:
            break
        
        density = predict(frame)

        payload = {
            "frame":frame_id,
            "density":int(density)
        }
        if density == 0:
            print("Predicted density: LOW")
        elif density == 1:
            print("Predicted density: MEDIUM")
        else:
            print("Predicted density: HIGH")

        requests.post("http://fog:5000/density", json=payload)

        frame_id += 1