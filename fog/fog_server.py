from flask import Flask, request
import requests
import time
import random

app = Flask(__name__)

FOG_TO_CLOUD_LATENCY_MS = (20, 80)  

def simulate_latency(min_ms, max_ms):
    time.sleep(random.uniform(min_ms, max_ms) / 1000)

def decision_engine(density):
    return {0: 60, 1: 40, 2: 20}[density]

@app.route("/density", methods=["POST"])
def receive():
    t_fog_recv = time.time()
    data = request.json

    density = data["density"]
    edge_ts = data.get("edge_ts", t_fog_recv)
    infer_ms = data.get("infer_ms", 0)

    t0 = time.time()
    signal_time = decision_engine(density)
    fog_proc_ms = (time.time() - t0) * 1000

    data["signal_time"] = signal_time
    data["fog_recv_ts"] = t_fog_recv
    data["fog_processing_ms"] = round(fog_proc_ms, 3)
    data["edge_to_fog_ms"] = round((t_fog_recv - edge_ts) * 1000, 3)

    simulate_latency(*FOG_TO_CLOUD_LATENCY_MS)  

    t_send = time.time()
    requests.post("http://cloud:6001/store", json=data)
    data["fog_to_cloud_ms"] = round((time.time() - t_send) * 1000, 3)

    print(f"Frame {data['frame']}", flush=True)
    print(f"Edge→Fog latency: {data['edge_to_fog_ms']:.2f}ms", flush=True)
    print(f"Fog processing: {fog_proc_ms:.2f}ms", flush=True)
    print(f"Fog→Cloud latency: {data['fog_to_cloud_ms']:.2f}ms", flush=True)
    print(flush=True)

    return {"status": "ok"}

app.run(host="0.0.0.0", port=5000)
