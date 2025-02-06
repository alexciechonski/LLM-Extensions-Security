import os
import json
import csv
from mitmproxy.io import FlowReader
from mitmproxy.websocket import WebSocketMessage

# Customizable parameters
EXTENSION_NAME = "copilot"
SPACE = "PublicSpaces"  # "PrivateSpaces", "PublicSpaces"

# Directory and file paths
FLOW_DIRECTORY = f"Copilot/{EXTENSION_NAME}"
OUTPUT_CSV = f"./Output/{EXTENSION_NAME}.csv"
OUTPUT_CSV_FP = f"{EXTENSION_NAME}-first-party.csv"
OUTPUT_CSV_TP = f"{EXTENSION_NAME}-third-party.csv"
DISCONNECT_JSON = "disconnect.json"


def load_disconnect_mapping(json_path):
    mapping_file = "disconnect_mapping.json"
    if os.path.exists(mapping_file):
        with open(mapping_file, "r", encoding="utf-8") as f:
            return json.load(f)

    with open(json_path, "r", encoding="utf-8") as f:
        disconnect_data = json.load(f)

    host_to_category = {}
    for category, entries in disconnect_data.get("categories", {}).items():
        for entry in entries:
            for host_dict in entry.values():
                for host_list in host_dict.values():
                    for host in host_list:
                        host_to_category[host] = category

    with open(mapping_file, "w", encoding="utf-8") as f:
        json.dump(host_to_category, f, indent=4)

    return host_to_category


def parse_flow_files(flow_dir, output_csv, output_csv_fp, output_csv_tp):
    disconnect_mapping = load_disconnect_mapping(DISCONNECT_JSON)

    output_rows = []
    headers_list = ["req_header_cookie", "res_header_cookie", "req_header_set-cookie", "res_header_set-cookie"]
    categories_of_interest = ["Advertising", "Analytics", "FingerprintingInvasive", "FingerprintingGeneral", "Social"]

    for filename in os.listdir(flow_dir):
        if not filename.startswith(EXTENSION_NAME) or not filename.endswith(".flow"):
            continue

        file_path = os.path.join(flow_dir, filename)

        with open(file_path, "rb") as file:
            try:
                reader = FlowReader(file)
            except Exception as e:
                print(f"Skipping invalid .flow file: {filename} ({e})")
                continue

            for flow in reader.stream():
                if not hasattr(flow, "request") or not flow.request:
                    continue

                request = flow.request
                response = flow.response
                timestamp = flow.request.timestamp_start

                if not timestamp:
                    continue

                request_domain = request.host
                request_url = request.url
                method = request.method
                status = response.status_code if response else None

                if response:
                    try:
                        size = len(response.content) if response.content else 0
                    except ValueError:
                        size = 0
                else:
                    size = 0

                cookies = request.cookies.fields

                try:
                    payload = request.content.decode("utf-8") if request.content else ""
                except UnicodeDecodeError:
                    payload = "[Binary or Non-UTF-8 Content]"

                request_headers = request.headers
                response_headers = response.headers if response else {}
                disconnect_category = disconnect_mapping.get(request_domain, "Other")
                origin_header = request_headers.get("origin", "")
                context = "Extension" if origin_header.startswith("chrome-extension://") else "Foreground"

                if context != "Extension" and disconnect_category not in categories_of_interest:
                    continue

                content_type = response_headers.get("content-type", "").lower()
                if content_type.startswith("text/html"):
                    response_body = "[HTML File/Code]"
                elif "javascript" in content_type or request_url.endswith(".js"):
                    response_body = "[Javascript File/Code]"
                elif "css" in content_type or request_url.endswith(".css"):
                    response_body = "[CSS File/Code]"
                elif content_type.startswith("image/"):
                    response_body = "[Media/Image]"
                elif content_type.startswith("video/"):
                    response_body = "[Media/Video]"
                else:
                    response_body = ""

                websocket_payloads = []
                if hasattr(flow, "websocket") and flow.websocket is not None:
                    for message in flow.websocket.messages:
                        if isinstance(message, WebSocketMessage):
                            websocket_payloads.append(message.content.decode("utf-8", errors="ignore"))

                websocket_combined = "\n".join(websocket_payloads)
                if websocket_combined and not payload:
                    payload = websocket_combined
                elif websocket_combined and payload:
                    payload += f"\n{websocket_combined}"

                row = {
                    "extension": EXTENSION_NAME,
                    "filename": filename,
                    "timestamp": timestamp,
                    "request_url": request_url,
                    "request_domain": request_domain,
                    "method": method,
                    "status": status,
                    "response": response_body,
                    "payload": payload,
                    "size": size,
                    "cookies": json.dumps(cookies),
                    "disconnect_category": disconnect_category,
                    "context": context,
                    "contacted_party": "first-party" if EXTENSION_NAME.lower() in request_domain else "third-party"
                }

                for header in headers_list:
                    if "req_header_" in header:
                        row[header] = request_headers.get(header.replace("req_header_", ""), "")
                    elif "res_header_" in header:
                        row[header] = response_headers.get(header.replace("res_header_", ""), "")

                output_rows.append(row)

    fieldnames = [
        "extension", "filename", "timestamp", "context", "disconnect_category",
        "contacted_party", "request_domain", "request_url", "method", "status",
        "response", "payload", "size", "cookies"
    ] + headers_list

    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)


if __name__ == "__main__":
    parse_flow_files(FLOW_DIRECTORY, OUTPUT_CSV, OUTPUT_CSV_FP, OUTPUT_CSV_TP)
    print(f"Output saved to {OUTPUT_CSV_FP} and {OUTPUT_CSV_TP}")