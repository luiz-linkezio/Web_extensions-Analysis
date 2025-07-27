import json

# Load the JSON of used permissions
file_path = "data/permissions_usage_report.json"  # Replace with the correct filename

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# List to store the usage rate of each extension
usage_rates = []

# Iterate over each extension
for ext_id, permissions in data.items():
    total_requested = len(permissions)  # Total permissions requested
    total_used = sum(1 for perm in permissions.values() if perm)  # Total permissions actually used

    # Avoid division by zero (in case an extension has no permissions listed)
    if total_requested > 0:
        usage_rate = total_used / total_requested
        usage_rates.append(usage_rate)

# Calculate the overall average usage rate
average_usage_rate = sum(usage_rates) / len(usage_rates) if usage_rates else 0

# Display the result
print(f"Average usage rate of requested permissions: {average_usage_rate:.2%}")
