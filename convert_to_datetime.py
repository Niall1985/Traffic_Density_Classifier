from datetime import datetime
import json

data_input = "logs\\pipeline_metrics_refactored.json"
data_output = "logs\\pipeline_metrics_refactored_with_datetime.json"

with open(data_input, "r") as f:
    content = f.read().strip()

try:
    records = json.loads(content)
except json.JSONDecodeError:
    records = [json.loads(line) for line in content.splitlines() if line.strip()]

ts_fields = ["cloud_recv_ts", "edge_ts", "fog_recv_ts"]

for record in records:
    for field in ts_fields:
        if field in record:
            ts = record[field]
            record[field] = datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S.%f")

with open(data_output, "w") as f:
    json.dump(records, f, indent=2)