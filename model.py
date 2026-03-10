import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import os
from sklearn.metrics import confusion_matrix, classification_report, precision_score, recall_score, f1_score
import seaborn as sns

os.makedirs("metrics", exist_ok=True)

dataset_path = "Augmented_Dataset"
img_size = (128, 128)
batch_size = 32
EPOCHS = 20

train_ds = tf.keras.utils.image_dataset_from_directory(
    os.path.join(dataset_path, "training"),
    image_size=img_size,
    color_mode="rgb",
    batch_size=batch_size,
    shuffle=True
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    os.path.join(dataset_path, "validation"),
    image_size=img_size,
    color_mode="rgb",
    batch_size=batch_size
)

test_ds = tf.keras.utils.image_dataset_from_directory(
    os.path.join(dataset_path, "testing"),
    image_size=img_size,
    color_mode="rgb",
    batch_size=batch_size,
    shuffle=False
)

class_names = train_ds.class_names
num_classes = len(class_names)

print("Classes:", class_names)

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.shuffle(1000, reshuffle_each_iteration=True)\
                   .prefetch(buffer_size=AUTOTUNE)

val_ds = val_ds.cache().prefetch(buffer_size=AUTOTUNE)
test_ds = test_ds.prefetch(buffer_size=AUTOTUNE)

data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomZoom(0.05),
])

model = tf.keras.Sequential([

    tf.keras.layers.Input(shape=(128, 128, 3)),
    data_augmentation,
    tf.keras.layers.Rescaling(1./255),

    tf.keras.layers.Conv2D(64, (3,3), padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(128, (3,3), padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(256, (3,3), padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.Conv2D(256, (3,3), padding='same'),
    tf.keras.layers.BatchNormalization(),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.MaxPooling2D(),

    tf.keras.layers.GlobalAveragePooling2D(),

    tf.keras.layers.Dense(256, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(1e-4)),
    tf.keras.layers.Dropout(0.3), 

    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0003),
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

callbacks = [
    tf.keras.callbacks.EarlyStopping(
        monitor='val_loss',
        patience=10,
        restore_best_weights=True,
        min_delta = 0.001
    ),
    tf.keras.callbacks.ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.5,
        patience=5,
        min_lr=1e-6,
        min_delta=0.001
    )
]

history = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=EPOCHS,
    callbacks=callbacks
)

test_loss, test_acc = model.evaluate(test_ds)
print("\nTesting Accuracy:", test_acc)

model.save("traffic_density_model.keras")

y_true = []
y_pred = []

for images, labels in test_ds:
    predictions = model.predict(images)
    predicted_labels = np.argmax(predictions, axis=1)
    y_true.extend(labels.numpy())
    y_pred.extend(predicted_labels)

precision = precision_score(y_true, y_pred, average='weighted')
recall    = recall_score(y_true, y_pred, average='weighted')
f1        = f1_score(y_true, y_pred, average='weighted')

print(f"Precision: {precision:.4f}")
print(f"Recall:    {recall:.4f}")
print(f"F1 Score:  {f1:.4f}")

with open("metrics/metrics.txt", "w") as f:

    f.write("=" * 50 + "\n")
    f.write("PER-EPOCH TRAINING & VALIDATION METRICS\n")
    f.write("=" * 50 + "\n")
    f.write(f"{'Epoch':<8}{'Train Acc':<14}{'Val Acc':<14}{'Train Loss':<14}{'Val Loss':<14}\n")
    f.write("-" * 60 + "\n")
    for ep in range(len(history.history['accuracy'])):
        f.write(
            f"{ep+1:<8}"
            f"{history.history['accuracy'][ep]:<14.4f}"
            f"{history.history['val_accuracy'][ep]:<14.4f}"
            f"{history.history['loss'][ep]:<14.4f}"
            f"{history.history['val_loss'][ep]:<14.4f}\n"
        )

    f.write("\n" + "=" * 50 + "\n")
    f.write("FINAL TRAINING & VALIDATION METRICS\n")
    f.write("=" * 50 + "\n")
    f.write(f"Final Training Accuracy   : {history.history['accuracy'][-1]:.4f}\n")
    f.write(f"Final Validation Accuracy : {history.history['val_accuracy'][-1]:.4f}\n")
    f.write(f"Final Training Loss       : {history.history['loss'][-1]:.4f}\n")
    f.write(f"Final Validation Loss     : {history.history['val_loss'][-1]:.4f}\n")

    f.write("\n" + "=" * 50 + "\n")
    f.write("TESTING METRICS\n")
    f.write("=" * 50 + "\n")
    f.write(f"Test Accuracy : {test_acc:.4f}\n")
    f.write(f"Test Loss     : {test_loss:.4f}\n")

    f.write("\n" + "=" * 50 + "\n")
    f.write("PRECISION, RECALL & F1 SCORE (weighted)\n")
    f.write("=" * 50 + "\n")
    f.write(f"Precision : {precision:.4f}\n")
    f.write(f"Recall    : {recall:.4f}\n")
    f.write(f"F1 Score  : {f1:.4f}\n")

    f.write("\n" + "=" * 50 + "\n")
    f.write("PER-CLASS CLASSIFICATION REPORT\n")
    f.write("=" * 50 + "\n")
    f.write(classification_report(y_true, y_pred, target_names=class_names))

cm = confusion_matrix(y_true, y_pred)

plt.figure(figsize=(6,5))
sns.heatmap(cm, annot=True, fmt='d',
            xticklabels=class_names,
            yticklabels=class_names)
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.savefig("metrics/confusion_matrix.png")
plt.close()

plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(history.history['accuracy'], label='Train Accuracy')
plt.plot(history.history['val_accuracy'], label='Val Accuracy')
plt.legend()
plt.title("Accuracy")

plt.subplot(1,2,2)
plt.plot(history.history['loss'], label='Train Loss')
plt.plot(history.history['val_loss'], label='Val Loss')
plt.legend()
plt.title("Loss")

plt.tight_layout()
plt.savefig("metrics/training_metrics.png")
plt.close()

print("\nAll metrics saved in 'metrics' folder.")