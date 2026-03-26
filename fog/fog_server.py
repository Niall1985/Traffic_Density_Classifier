from flask import Flask, request
import requests

app = Flask(__name__)

def decision_engine(density):
    mapping = {
        0:20,
        1:40,
        2:60
    }

    return mapping[density]

@app.route("/density", methods=["POST"])
def receive():
    data = request.json
    density = data["density"]
    signal_time = decision_engine(density)
    data["signal_time"] = signal_time
    print("Received density:", density)
    print("Signal time:", signal_time)
    
    requests.post("http://cloud:6000/store", json=data)
    
    return {"status":"ok"}

app.run(host="0.0.0.0", port=5000)
