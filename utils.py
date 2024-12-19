import os
import subprocess
import json
from mitmproxy.io import FlowReader
from mitmproxy.http import HTTPFlow

def combine_flows(folder_path, output_file):
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")

    files_to_combine = [
        os.path.join(folder_path, filename)
        for filename in os.listdir(folder_path)
        if filename.endswith('.flow')  
    ]
    input_files = " ".join(files_to_combine)
    output_file_path = os.path.join(folder_path, output_file)

    command = f"cat {input_files} > {output_file_path}"
    print(command)
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"Combined flows saved to {output_file_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error combining flows: {e}")

def flow2json(input_path, output_path):
    items = []
    with open(input_path, "rb") as logfile:
        freader = flow.FlowReader(logfile)
        try:
            for f in freader.stream():
                items.append( f )
        except Exception as e:
            print("Flow file corrupted: {}".format(e))
    return items


if __name__ == "__main__":
    import json
    with open('harpa.flow', "rb") as file:
            reader = FlowReader(file)

    for flow in reader.stream():
        print(flow)