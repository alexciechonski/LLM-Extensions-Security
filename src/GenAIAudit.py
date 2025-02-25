from analysis import NetworkAnalyzer
from flow_processor import FlowProcessor
import pandas as pd
import argparse
import os
import tempfile
import subprocess
from mitmproxy.io import FlowReader
from mitmproxy.http import HTTPFlow
import time
import threading
import json

class GenAIAudit:
    def __init__(self, extension, run_gui=False) -> None:
        self.extension = extension
        self.processor = FlowProcessor(self.extension)
        self.gui = run_gui

    @staticmethod
    def start_proxy():
        flow_path = os.path.join(os.getcwd(), "working.flow")
        if os.path.exists(flow_path):
            print("path exist")
        else:
            print('bad path')
        time.sleep(3)

        try:
            proxy_process = subprocess.Popen(["mitmweb", "-w", flow_path]) # change to mitmproxy

            # Keep function alive until mitmproxy stops
            while proxy_process.poll() is None:
                time.sleep(1)

        except KeyboardInterrupt:
            print("\nCtrl + C detected. Stopping mitmproxy...")
            proxy_process.terminate()
            proxy_process.wait()
        except subprocess.CalledProcessError as e:
            print(f"Error running mitmproxy: {e}")
            

    @staticmethod
    def delete_file(file_name):
        pass
    
    def run(self):
        res = {}
        flow = self.start_proxy()
        print("Starting analysis.")
        processor = FlowProcessor(
            extension_name=self.extension,
        )
        df = processor.process_flows(flow)
        analyzer = NetworkAnalyzer(df, None, flow, self.extension)
        res = analyzer.run()
        self.repr(res)
        return

def main():
    audit = GenAIAudit('maxai')
    # audit.start_proxy()
    # df = audit.processor.process_flows("working.flow")
    # df.to_csv('max_test.csv')
    # print(df)
    # print(df['contacted_party'])

    # analsysis
    df = pd.read_csv('processed_max.csv')
    analyzer = NetworkAnalyzer(df, "MaxAI/max-lin-search-new.flow", audit.extension)
    fp, tp = analyzer.run()

    json_args = json.dumps({"fp": fp, "tp": tp})

    # Step 3: Run Streamlit as a subprocess, passing JSON as an argument
    subprocess.Popen(["streamlit", "run", "src/app.py", "--", json_args], start_new_session=True)





if __name__ == "__main__":
    main()


"""
TODO:
1. fix the bug with processor
2. get argparse to work
3. remove changing wi-fi
4. better gui using js
5. temp file
5. better payload viewing
"""