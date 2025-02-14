import pandas as pd    
from collections import defaultdict
from flow_processor import FlowProcessor
import json
from mitmproxy.io import FlowReader
from mitmproxy.http import HTTPFlow
import ollama
from src.utils import *

class NetworkAnalyzer():
    def __init__(self, df, csv_path, flow_file, extension) -> None:
        self.network = df if df else pd.read_csv(csv_path)
        self.res = defaultdict(set)        
        self.extension = extension
        self.flow_file = flow_file

    def get_referer(self, target_domain):
        res = []
        with open(self.flow_file, "rb") as file:
            reader = FlowReader(file)
            
            # Loop through the flows to find requests matching the target domain
            for flow in reader.stream():
                if not hasattr(flow, "request") or not flow.request:
                    continue

                # Check if the request's host matches the target domain
                if target_domain in flow.request.host:
                    referer_header = flow.request.headers.get("Referer")
                    if referer_header:
                        res.append(referer_header)
        return res
        
    def remove_noise(self, domains: set):
        res = []
        for domain in domains:
            if any(self.extension in ref for ref in self.get_referer(domain)):
                res.append(domain)
        return res

    def get_party(self, party):
        df = self.network
        df = df[
            (df['contacted_party'] == f'{party}-party')
        ]
        domains = set(df['request_domain'].tolist())
        return self.remove_noise(domains)

    def get_all_payloads(self, endpoint):
        request_payloads = []
        # seen = {} # (set(keys):memory_size)
        try:
            with open(self.flow_file, "rb") as f:
                reader = FlowReader(f)
                
                for flow in reader.stream():
                    if not isinstance(flow, HTTPFlow):
                        continue

                    if endpoint not in flow.request.url:
                        continue

                    try:
                        request_data = json.loads(flow.request.content.decode('utf-8'))
                        request_payloads.append(request_data)
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        pass

        except Exception as e:
            print(f"Error processing flow file: {e}")
        print(len(request_payloads))
        return request_payloads

    def process_payloads(self, payloads: str):
        try:
            prompt = get_base_prompt("src/prompt.txt") + payloads
            response = ollama.chat(model='tinyllama', messages=[{"role": "user", "content": prompt}])
            return response['message']['content']  # Extract the generated response
        except Exception as e:
            return f"Error communicating with Ollama: {e}"

    def get_summary(self, endpoints: list[str]):
        payload_str = ""
        payloads = [self.get_all_payloads(endpoint) for endpoint in endpoints]
        for payload in payloads:
            payload_str += str(payload) + '\n'
        return self.process_payloads(payload_str)

    # def get_cookies(self, endpoint):
    #     pass

    def process_llm_resp(resp):
        pass

    def run(self):
        first_parties = self.get_party('first')
        fp_summary = self.get_summary(first_parties)

        third_parties = self.get_party('third')
        tp_summary = self.get_summary(third_parties)

        return {
            'first-party':fp_summary,
            'third-party': tp_summary
        }


def main():
    na = NetworkAnalyzer(None, 'harpa.csv', 'Harpa/harpa-lin-search-new.flow', "Harpa")

    with open('all_payloads.json', 'r') as f:
        payloads = json.load(f)

    payload_str = str(payloads[0])
    
    # print(payload_str)

    response = ollama.chat(model='tinyllama', messages=[{"role": "user", "content": get_base_prompt('src/prompt.txt') + payload_str}])
    print(response['message']['content'])
    
    
if __name__ == "__main__":
   main()

"""
TODO:
1. create a cli tool
2. fill out prompt.txt based on the paper
3. get cookies function
4. represent the output
"""