from analysis import NetworkAnalyzer
from flow_processor import FlowProcessor
import pandas as pd
import argparse
import os

class GenAIAudit:
    def __init__(self, extension) -> None:
        self.extension = extension

    @staticmethod
    def get_flow():
        pass

    @staticmethod
    def repr(res):
        pass
    
    def run(self):
        res = {}
        flow = self.get_flow()
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
    parser = argparse.ArgumentParser(description="Audit AI-based extensions")
    parser.add_argument("extensions", type=str, help="Comma-separated list of extensions to audit")
    
    args = parser.parse_args()
    extensions = args.extensions.split(",")

    print("Starting analysis...")
    for ext in extensions:
        ext = ext.strip()
        print(ext)

if __name__ == "__main__":
    main()