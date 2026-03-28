# 🚦 Traffic Density Classification — TinyML Edge Deployment

A TinyML-enabled traffic density classification system that uses a lightweight
Convolutional Neural Network (CNN) to classify traffic conditions (Low, Medium, High)
directly from camera images at the edge, optimized for deployment via TensorFlow Lite.

---

## 📁 Project Structure
```
TRAFFIC_DE.../
├── Augmented_Dataset/
│   ├── training/
│   ├── validation/
│   └── testing/
├── cloud/
│   ├── cloud_server.py
│   ├── Dockerfile
│   └── requirements.txt
├── edge/
│   ├── edge_inference.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── traffic_density_model.tflite
│   ├── high.jpg
│   ├── low.jpg
│   ├── traffic.mp4
│   └── traffic1.mp4
├── fog/
│   ├── fog_server.py
│   ├── Dockerfile
│   └── requirements.txt
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
├── docker-compose.yml              # Multi-node simulation
├── high.jpg                        # Sample high density image
├── mid.jpg                         # Sample medium density image
├── low.jpg                         # Sample low density image
├── traffic_density_model.keras     # Trained float32 Keras model
├── traffic_density_model.tflite    # Dynamic range quantized model
├── traffic_density_model_int8...   # Full INT8 quantized TFLite model
└── requirements.txt
```

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

---

## 🐳 Simulating Edge–Fog–Cloud Architecture with Docker

The project includes a full multi-node simulation using Docker Compose, where
each layer of the Edge–Fog–Cloud architecture runs as an isolated container on
your local machine.

### Architecture
```
[Edge Container]
  └── Runs TFLite inference on sample images/video frames
  └── Classifies traffic as Low / Medium / High
  └── POSTs result to Fog node every inference cycle

[Fog Container]
  └── Receives density results from one or more Edge nodes
  └── Aggregates and buffers readings
  └── Forwards consolidated data to Cloud node

[Cloud Container]
  └── Stores all incoming density records
  └── Exposes a REST API for querying historical data
  └── Acts as the central analytics and retraining endpoint
```

### Node responsibilities

| Node | Container | Role |
|---|---|---|
| Edge | `edge/` | TFLite inference, sends predictions |
| Fog | `fog/` | Aggregation, regional coordination |
| Cloud | `cloud/` | Storage, analytics, retraining endpoint |

### How to run the simulation

**1. Make sure Docker Desktop is running**

**2. Build and start all three nodes:**
```bash
docker-compose up --build
```

This starts all three containers on an isolated Docker network. The edge node
begins inference immediately and sends results to the fog node, which forwards
them to the cloud node.

**3. Watch the logs from each node:**
```bash
# All nodes together
docker-compose logs -f

# Individual nodes
docker-compose logs -f edge
docker-compose logs -f fog
docker-compose logs -f cloud
```

**4. Stop all nodes:**
```bash
docker-compose down
```

### Environment variables

To suppress verbose TensorFlow startup messages, set the following in your
shell or in the edge service environment block in `docker-compose.yml`:
```bash
TF_ENABLE_ONEDNN_OPTS=0
PYTHONUNBUFFERED=1
```

`PYTHONUNBUFFERED=1` is important — without it, print output from the edge
node may not appear in Docker logs due to stdout buffering.

### docker-compose.yml overview
```yaml
version: "3.9"

services:
  edge:
    build: ./edge
    depends_on:
      - fog
    environment:
      - PYTHONUNBUFFERED=1
      - TF_ENABLE_ONEDNN_OPTS=0

  fog:
    build: ./fog
    depends_on:
      - cloud
    ports:
      - "5000:5000"

  cloud:
    build: ./cloud
    ports:
      - "6000:6000"
```

All three services share Docker's default bridge network, so the edge node
reaches the fog node at `http://fog:5000` and the fog node reaches the cloud
at `http://cloud:6000` — no IP addresses needed.

### Expected log output

A healthy simulation looks like this:
```
cloud-1  | * Running on http://0.0.0.0:6000
fog-1    | * Running on http://0.0.0.0:5000
edge-1   | INFO: Created TensorFlow Lite XNNPACK delegate for CPU.
edge-1   | Predicted Traffic Level: Low
edge-1   | Confidence: 99.28%
fog-1    | POST /density HTTP/1.1 200 -
cloud-1  | POST /store HTTP/1.1 200 -
edge-1   | exited with code 0
```

---

## 📦 Requirements
```
tensorflow 
opencv-python 
matplotlib 
scikit-learn

```
Install via:
```bash
pip install -r requirements.txt
```

---

## 📄 License

This project is licensed under the terms of the MIT LICENSE file included in this repository.