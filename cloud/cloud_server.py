# from flask import Flask, request

# app = Flask(__name__)

# @app.route("/store", methods=['POST'])
# def store():
#     data = request.json
#     print("Cloud received: ", data, flush=True)
#     return {"saved":True}

# app.run(host="0.0.0.0", port=6000)

# from flask import Flask, request, jsonify
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)

# records = []

# @app.route("/store", methods=['POST'])
# def store():
#     data = request.json
#     records.append(data)
#     print("Cloud received: ", data, flush=True)
#     return {"saved": True}

# @app.route("/data", methods=['GET'])
# def get_data():
#     return jsonify(records)

# app.run(host="0.0.0.0", port=6001)







from flask import Flask, request, jsonify
from flask_cors import CORS
import time
import os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

records = []


LOG_DIR  = "/app/logs"
LOG_FILE = os.path.join(LOG_DIR, "pipeline_log.txt")
os.makedirs(LOG_DIR, exist_ok=True)

def log(msg):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

@app.route("/store", methods=["POST"])
def store():
    t_cloud_recv = time.time()
    data = request.json

    edge_ts = data.get("edge_ts", t_cloud_recv)
    data["cloud_recv_ts"]     = t_cloud_recv
    data["total_pipeline_ms"] = round((t_cloud_recv - edge_ts) * 1000, 3)

    records.append(data)

    log(f"Frame {data['frame']}")
    log(f"  Class:            {data.get('density')} | Signal: {data.get('signal_time')}s")
    log(f"  Inference:        {data.get('infer_ms', '?')}ms")
    log(f"  Edge→Fog:         {data.get('edge_to_fog_ms', '?')}ms")
    log(f"  Fog processing:   {data.get('fog_processing_ms', '?')}ms")
    log(f"  Fog→Cloud:        {data.get('fog_to_cloud_ms', '?')}ms")
    log(f"  TOTAL PIPELINE:   {data['total_pipeline_ms']}ms")
    log(f"  {'─' * 40}")

    return {"saved": True}

@app.route("/data", methods=["GET"])
def get_data():
    return jsonify(records)

@app.route("/latency", methods=["GET"])
def get_latency():
    if not records:
        return jsonify({"error": "no data yet"})
    totals = [r["total_pipeline_ms"] for r in records if "total_pipeline_ms" in r]
    infers = [r["infer_ms"] for r in records if "infer_ms" in r]
    summary = {
        "frames":           len(records),
        "avg_pipeline_ms":  round(sum(totals) / len(totals), 2),
        "max_pipeline_ms":  round(max(totals), 2),
        "min_pipeline_ms":  round(min(totals), 2),
        "avg_inference_ms": round(sum(infers) / len(infers), 2),
    }
    log("── LATENCY SUMMARY ──────────────────────────")
    for k, v in summary.items():
        log(f"  {k}: {v}")
    log("─────────────────────────────────────────────")
    return jsonify(summary)

app.run(host="0.0.0.0", port=6001)