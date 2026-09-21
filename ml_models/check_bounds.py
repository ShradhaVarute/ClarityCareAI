import json

with open("feature_bounds_generated.json") as f:
    data = json.load(f)

for k, v in data["heart_disease"].items():
    print(k, v)