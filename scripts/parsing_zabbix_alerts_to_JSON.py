import json
import re

# Safely retrieve the full input node passed from Shuffle
nodevalue = r"""$exec"""
jsondata = json.loads(nodevalue)
message_content = jsondata.get("message", "")

# Dictionary to store all extracted fields
extracted_data = {}

# Regex patterns used to extract each field from the raw alert text
patterns = {
    "event_id": r"Problem ID\s+(\d+)",                          # Unique Zabbix problem/event ID
    "problem_name": r"event named\s+(.*?)\.",                   # Name/title of the triggered event
    "time": r"started at\s+([\d:]+)",                           # Time the problem started (HH:MM:SS)
    "date": r"on\s+([\d.]+)",                                   # Date the problem started
    "severity": r"severity level of\s+(\w+)",                   # Severity level (e.g. High, Warning)
    "ioc": r"applied from\s+(.*?)\s+and is ongoing",             # Indicator of Compromise / source condition
    "host_name": r"ongoing on host\s+([\w-]+)",                  # Affected host name
    "host_id": r"identified by ID no\s+(\d+)",                   # Affected host's Zabbix ID
    "host_ip": r"with IP address\s+([\d\.:a-fA-F]+)",            # Affected host's IP address
    "cpu_usage": r"CPU usage of\s+([\d.]+)\s*%",                 # CPU usage percentage at time of alert
    "inbound_traffic": r"inbound traffic of\s+(\d+)\s*bps",      # Inbound network traffic (bits per second)
    "outbound_traffic": r"outbound traffic of\s+(\d+)\s*bps",    # Outbound network traffic (bits per second)
    "info_url": r"by this link:\s*(https?://[^\s]+)"             # URL to the Zabbix event details page
}

# Run each pattern against the alert message and collect the results.
# Any field that isn't found is set to "N/A" so the output JSON always
# has a consistent, predictable structure for downstream Shuffle steps.
for key, pattern in patterns.items():
    match = re.search(pattern, message_content)
    if match:
        extracted_data[key] = match.group(1).strip().replace('"', '')
    else:
        extracted_data[key] = "N/A"

# Output the structured data as JSON so Shuffle can consume it in the next step
print(json.dumps(extracted_data))