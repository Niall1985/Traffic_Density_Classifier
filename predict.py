import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image

model = tf.keras.models.load_model("traffic_density_model.keras")

class_names = ["High", "Low", "Medium"]

img_path = "low.jpg"

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

# import tensorflow as tf
# import numpy as np
# from tensorflow.keras.preprocessing import image

# # Load TFLite model
# interpreter = tf.lite.Interpreter(model_path="traffic_density_model.tflite")
# interpreter.allocate_tensors()

# # Get input and output details
# input_details = interpreter.get_input_details()
# output_details = interpreter.get_output_details()

# class_names = ["High", "Low", "Medium"]

# img_path = "low.jpg"

# # Load image
# img = image.load_img(
#     img_path,
#     target_size=(128, 128),
#     color_mode="rgb"
# )

# # Convert image to array
# img_array = image.img_to_array(img)

# # Normalize (important for most models)
# img_array = img_array / 255.0

# # Add batch dimension
# img_array = np.expand_dims(img_array, axis=0).astype(np.float32)

# # Set input tensor
# interpreter.set_tensor(input_details[0]['index'], img_array)

# # Run inference
# interpreter.invoke()

# # Get prediction
# prediction = interpreter.get_tensor(output_details[0]['index'])

# predicted_index = np.argmax(prediction)
# predicted_class = class_names[predicted_index]
# confidence = np.max(prediction) * 100

# print("Predicted Traffic Level:", predicted_class)
# print("Confidence: {:.2f}%".format(confidence))