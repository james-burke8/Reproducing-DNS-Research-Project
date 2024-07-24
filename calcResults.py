import json
from resolver import *

# Load the JSON data
with open('error_free_domains.json', 'r') as f:
    data = json.load(f)

percent_affected, percent_unreachable = calculate_metrics_from_json(data)

print("Percent Affected by AS Organization:")
top_10_items = dict(sorted(percent_affected.items(), key=lambda x: x[1], reverse=True)[:10])
print(json.dumps(top_10_items, indent=4))

print("\nPercent Unreachable by AS Organization:")
top_10_items2 = dict(sorted(percent_unreachable.items(), key=lambda x: x[1], reverse=True)[:10])
print(json.dumps(top_10_items2, indent=4))
