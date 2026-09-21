import json

with open("feature_bounds_generated.json") as f:
    data = json.load(f)

with open("../backend/app/core/feature_bounds.py", "w") as f:
    f.write("FEATURE_BOUNDS = {\n")
    for disease, features in data.items():
        f.write(f'    "{disease}": {{\n')
        for feat, (lo, hi) in features.items():
            f.write(f"        {feat!r}: ({lo}, {hi}),\n")
        f.write("    },\n")
    f.write("}\n")

print("feature_bounds.py regenerated with real training-data bounds")