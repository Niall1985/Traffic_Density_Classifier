# from flask import Flask, request

# app = Flask(__name__)

# @app.route("/store", methods=['POST'])
# def store():
#     data = request.json
#     print("Cloud received: ", data, flush=True)
#     return {"saved":True}

# app.run(host="0.0.0.0", port=6000)

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

records = []

@app.route("/store", methods=['POST'])
def store():
    data = request.json
    records.append(data)
    print("Cloud received: ", data, flush=True)
    return {"saved": True}

@app.route("/data", methods=['GET'])
def get_data():
    return jsonify(records)

app.run(host="0.0.0.0", port=6001)