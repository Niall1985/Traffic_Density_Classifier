# 🚦 Traffic Density Classification — TinyML Edge Deployment

A TinyML-enabled traffic density classification system that uses a lightweight
Convolutional Neural Network (CNN) to classify traffic conditions (Low, Medium, High)
directly from camera images at the edge, optimized for deployment via TensorFlow Lite.

---

## 📁 Project Structure

TRAFFIC_DE.../
├── Augmented_Dataset/
│   ├── training/
│   ├── validation/
│   └── testing/
├── Final_Dataset/
├── metrics/
│   ├── confusion_matrix.png
│   ├── metrics.txt
│   └── training_metrics.png
├── testcodes/
├── model.py                        # CNN model definition and training
├── quantize.py                     # Full INT8 quantization via TFLite
├── convert_to_tinyml.py            # Dynamic range TFLite conversion
├── image_augment.py                # Dataset augmentation script
├── clean_dataset.py                # Dataset cleaning utility
├── predict.py                      # Run inference on sample images
├── high.jpg                        # Sample high density image
├── mid.jpg                         # Sample medium density image
├── low.jpg                         # Sample low density image
├── traffic_density_model.keras     # Trained float32 Keras model
├── traffic_density_model.tflite    # Dynamic range quantized model
├── traffic_density_model_int8...   # Full INT8 quantized TFLite model
└── requirements.txt


---

## 🧠 Model

A custom CNN trained to classify traffic density into three classes:

| Class | Description |
|---|---|
| 🟢 Low | Light traffic, few vehicles |
| 🟡 Medium | Moderate traffic flow |
| 🔴 High | Heavy congestion |

**Architecture:**
- Conv2D (64) → Conv2D (128) → Conv2D (256) → Conv2D (256)
- BatchNormalization + ReLU + MaxPooling after each Conv block
- GlobalAveragePooling → Dense (256) → Dropout (0.3) → Softmax
- Input size: 128×128×3

---

## ⚙️ Setup

### 1. Clone the repository
```bash
git clone https://github.com/Niall1985/traffic-density-classifier.git
cd traffic-density-classifier
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Prepare dataset
Place your dataset in the following structure:
```
Augmented_Dataset/
├── training/
│   ├── low/
│   ├── medium/
│   └── high/
├── validation/
└── testing/
```
Or run the augmentation script on your raw dataset:
```bash
python image_augment.py
```

---

## 🚀 Usage

### Train the model
```bash
python model.py
```
Outputs `traffic_density_model.keras` and saves metrics to `metrics/`.

### Convert to TFLite (dynamic range)
```bash
python convert_to_tinyml.py
```
Outputs `traffic_density_model.tflite`

### Convert to INT8 TFLite (full quantization)
```bash
python quantize.py
```
Outputs `traffic_density_model_int8.tflite` — optimized for microcontrollers.

### Run inference
```bash
python predict.py
```
Uses sample images (`low.jpg`, `mid.jpg`, `high.jpg`) to test the model.

---

## 📊 Metrics

Training metrics, per-epoch accuracy/loss, precision, recall, F1 score,
and a confusion matrix are all saved automatically to the `metrics/` folder
after training.

| Metric | Value |
|---|---|
| Test Accuracy | _see metrics/metrics.txt_ |
| Precision | _see metrics/metrics.txt_ |
| Recall | _see metrics/metrics.txt_ |
| F1 Score | _see metrics/metrics.txt_ |

---

## 🔬 TinyML Deployment

| Model | Type | Size | Target Hardware |
|---|---|---|---|
| `.keras` | float32 | ~X MB | Training only |
| `.tflite` | Dynamic range | ~X/2 MB | Raspberry Pi |
| `_int8.tflite` | Full INT8 | ~X/4 MB | ESP32, Arduino, Coral TPU |

### Edge–Fog–Cloud Architecture

```
[Traffic Camera]
      ↓ capture frame
[Edge Device — Raspberry Pi / ESP32]
      ↓ INT8 TFLite inference
[Low / Medium / High]
      ↓ adaptive signal control
[Fog Layer — regional coordinator]
      ↓ aggregated traffic data
[Cloud — model retraining & analytics]
```

---

## 📦 Requirements

```
tensorflow
numpy
scikit-learn
matplotlib
seaborn
```
Install via:
```bash
pip install -r requirements.txt
```

---

## 📄 License

This project is licensed under the terms of the LICENSE file included
in this repository.

---

