from flask import Flask, request

app = Flask(__name__)

@app.route("/store", methods=['POST'])
def store():
    data = request.json
    print("Cloud received: ", data)
    return {"saved":True}

app.run(host="0.0.0.0", port=6000)