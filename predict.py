import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

model = tf.keras.models.load_model("traffic_density_model.keras")

class_names = ["High", "Low", "Medium"]

img_path = "high.jpg"

img = image.load_img(
    img_path,
    target_size=(128, 128), 
    color_mode="rgb"          
)

img_array = image.img_to_array(img)

img_array = np.expand_dims(img_array, axis=0)

prediction = model.predict(img_array)

predicted_index = np.argmax(prediction)
predicted_class = class_names[predicted_index]
confidence = np.max(prediction) * 100

print("Predicted Traffic Level:", predicted_class)
print("Confidence: {:.2f}%".format(confidence))