import tensorflow as tf
import numpy as np

model = tf.keras.models.load_model("traffic_density_model.keras")

converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
def representative_data_gen():
    for _ in range(100):
        dummy_input = np.random.rand(1, 128, 128, 3).astype(np.float32)
        yield [dummy_input]

converter.representative_dataset = representative_data_gen

converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
converter.inference_input_type = tf.int8
converter.inference_output_type = tf.int8

tflite_model = converter.convert()

with open("traffic_density_model_int8.tflite", "wb") as f:
    f.write(tflite_model)

print("INT8 model saved.")