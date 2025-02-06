from analysis import networkAnalyzer
from flow_processor import FlowProcessor
import pandas as pd

def main():
    processor = FlowProcessor(
        extension_name="copilot",
        flow_directory="Copilot",
        output_csv="src/copilot.csv",
        disconnect_json="src/disconnect.json"
    )
    df = processor.process_flows("Copilot/copilot-lin-control.flow")
    print(df == pd.read_csv("src/copilot.csv"))


if __name__ == "__main__":
    main()