import time
import random
import cv2
import requests
import tensorflow as tf
import numpy as np

EDGE_TO_FOG_LATENCY_MS = (5, 20)

def simulate_latency(min_ms, max_ms):
    time.sleep(random.uniform(min_ms, max_ms) / 1000)


interpreter = tf.lite.Interpreter(model_path="traffic_density_model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
class_names = ["High", "Medium", "Low"]

def predict(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (128, 128), interpolation=cv2.INTER_LINEAR)
    img = np.expand_dims(img, axis=0).astype(np.float32)
    t0  = time.time()
    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    infer_ms = (time.time() - t0) * 1000
    return np.argmax(output), np.max(output) * 100, infer_ms


video = cv2.VideoCapture("traffic_main.mp4")
frame_id = 0

while True:
    if frame_id == 3000:
        break
    ret, frame = video.read()
    if not ret:
        break

    t_frame_start = time.time()
    density_index, confidence, infer_ms = predict(frame)
    predicted_class = class_names[density_index]

    payload = {
        "frame": frame_id,
        "density": int(density_index),
        "edge_ts": time.time(),
        "infer_ms": round(infer_ms, 3),
    }

    simulate_latency(*EDGE_TO_FOG_LATENCY_MS)   

    t_send = time.time()
    requests.post("http://fog:5000/density", json=payload)
    edge_to_fog_ms = (time.time() - t_send) * 1000
    total_ms = (time.time() - t_frame_start) * 1000

    print(f"Frame {frame_id}", flush=True)
    print(f"Predicted: {predicted_class} ({confidence:.2f}%)", flush=True)
    print(f"Inference: {infer_ms:.2f}ms", flush=True)
    print(f"Edge→Fog send: {edge_to_fog_ms:.2f}ms", flush=True)
    print(f"Total (edge): {total_ms:.2f}ms", flush=True)
    print(flush=True)

    frame_id += 1

video.release()