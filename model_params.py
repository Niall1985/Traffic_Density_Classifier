import tensorflow as tf

model = tf.keras.models.load_model("traffic_density_model.keras")

print(model.summary())