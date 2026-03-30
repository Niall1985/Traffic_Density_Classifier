import cv2
import requests
import tensorflow as tf
import numpy as np

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="traffic_density_model.tflite")
interpreter.allocate_tensors()

# Get tensor details once
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Correct class order (same as training)
class_names = ["High", "Medium", "Low"]

def predict(img):
   
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    img = cv2.resize(img, (128, 128), interpolation=cv2.INTER_LINEAR)

    img = np.expand_dims(img, axis=0).astype(np.float32)

    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()

    output = interpreter.get_tensor(output_details[0]['index'])
    return np.argmax(output), np.max(output) * 100


video = cv2.VideoCapture("traffic.mp4")

frame_id = 0

while True:

    if frame_id == 3500:
        break

    ret, frame = video.read()
    if not ret:
        break

    density_index, confidence = predict(frame)
    predicted_class = class_names[density_index]

    payload = {
        "frame": frame_id,
        "density": int(density_index)
    }

    print(f"Frame {frame_id}")
    print("Predicted Traffic Level:", predicted_class, flush=True)
    print("Confidence: {:.2f}%".format(confidence), flush=True)
    print()

    # Send to fog node
    requests.post("http://fog:5000/density", json=payload)

    frame_id += 1

video.release()


# import cv2
# import requests
# import tensorflow as tf
# import numpy as np

# interpreter = tf.lite.Interpreter(model_path="traffic_density_model.tflite")
# interpreter.allocate_tensors()

# # Get tensor details
# input_details = interpreter.get_input_details()
# output_details = interpreter.get_output_details()

# # Correct class order (same as training)
# class_names = ["High", "Low", "Medium"]

# def predict(img):
   
#     img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     img = cv2.resize(img, (128, 128), interpolation=cv2.INTER_LINEAR)

#     img = np.expand_dims(img, axis=0).astype(np.float32)

#     interpreter.set_tensor(input_details[0]['index'], img)
#     interpreter.invoke()

#     output = interpreter.get_tensor(output_details[0]['index'])
#     return np.argmax(output), np.max(output) * 100


# image_path = "low.jpg"
# image = cv2.imread(image_path)

# if image is None:
#     print("Error loading image")
#     exit()

# density_index, confidence = predict(image)

# predicted_class = class_names[density_index]

# # Prepare payload
# payload = {
#     "frame": 0,
#     "density": int(density_index)
# }

# print("Predicted Traffic Level:", predicted_class, flush=True)
# print("Confidence: {:.2f}%".format(confidence), flush=True)

# # Send result to fog node
# requests.post("http://fog:5000/density", json=payload)