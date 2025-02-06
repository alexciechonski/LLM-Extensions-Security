from mitmproxy.io import FlowReader
import socket
import json


file_path = "Copilot/copilot-lin-control.flow"
output_file = "x.json"

# Dictionary to store destinations, associated IPs, and counts
destinations = {}

with open(file_path, "rb") as f:
    reader = FlowReader(f)
    for flow in reader.stream():
        if hasattr(flow, "request") and flow.request:
            host = flow.request.host
            try:
                ip_address = socket.gethostbyname(host)
            except socket.gaierror:
                ip_address = "IP not found"

            if host in destinations:
                destinations[host]['count'] += 1
            else:
                destinations[host] = {
                    'ip': ip_address,
                    'count': 1,
                }

        elif hasattr(flow, "client_conn"):
            # Using peername instead of address to resolve DeprecationWarning
            ip_address = flow.client_conn.peername[0]

            if ip_address in destinations:
                destinations[ip_address]['count'] += 1
            else:
                destinations[ip_address] = {
                    'ip': ip_address,
                    'count': 1,
                }

# Write results to a JSON file
with open(output_file, "w") as output:
    json.dump(destinations, output, indent=4)

print(f"Results saved to {output_file}")