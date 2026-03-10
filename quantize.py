import tensorflow as tf
import numpy as np
import os

model = tf.keras.models.load_model("traffic_density_model.keras")

calib_ds = tf.keras.utils.image_dataset_from_directory(
    os.path.join("Augmented_Dataset", "training"),
    image_size=(128, 128),
    batch_size=1,
    shuffle=True
)

def representative_data_gen():
    for images, _ in calib_ds.take(200):          
        img = tf.cast(images, tf.float32) / 255.0  
        yield [img]

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.representative_dataset = representative_data_gen
converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type  = tf.int8
converter.inference_output_type = tf.int8

tflite_model = converter.convert()

with open("traffic_density_model_int8.tflite", "wb") as f:
    f.write(tflite_model)

print(f"INT8 model saved — size: {len(tflite_model) / 1024:.2f} KB")