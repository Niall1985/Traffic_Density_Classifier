import json

with open("logs\\pipeline_metrics.json") as f:
    data = json.loads(f.read())

with open("logs\\pipeline_metrics_refactored.json", "w") as f:
    for obj in data:
        json.dump(obj, f)
        f.write("\n")