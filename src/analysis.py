import pandas as pd    
from collections import defaultdict
from flow_processor import FlowProcessor
import json
from mitmproxy.io import FlowReader
from mitmproxy.http import HTTPFlow

"""
{'Max.AI-lin-search-new.flow', 'Max.AI-Lin-Summarize.flow', 'Max.AI-Lin-Browse.flow'}
{'Harpa-lin-summarizing.flow', 'Harpa-lin-search-new.flow', 'Harpa-Lin-control.flow', 'Harpa-Lin-browse.flow'}
{'Copilot-lin-control.flow', 'Copilot-lin-summary.flow', 'Copilot-lin-search_new.flow', 'Copilot-lin-browse.flow'}
"""

# df = pd.read_csv(
#     # "flow_csvs/Max.AI.csv"
#     # "flow_csvs/Harpa.csv"
#     # "flow_csvs/Copilot.csv"
#     'summary.csv'
#     )

# filtered_df = df[
#     (df['contacted_party'] == 'third-party')
#     & (df['filename'] == 'Copilot-lin-browse.flow')
#     # & (df['req_header_referer'] != "https://temp-mail.org/")
#     # & (df['req_header_referer'] != "https://chromewebstore.google.com/")
#     ]
# request_domains = filtered_df['request_domain'].tolist()
# rd = set(request_domains)

# print(rd)


class networkAnalyzer():
    def __init__(self, network, flow_file, extension) -> None:
        self.network = network
        """
        self.struct = {
            "domain_of_page": set(),
            "page_content": set(),
            "google_search_results": set(),
            "users_query": set(),
            "user_details": set(),
            "device_details": set(),
            "time_of_query": set(),
            "timezone": set(),
            "context_text": set(),
            "chat_history": set(),
            "chat_id": set(),
            "page_referrer": set(),
            "user_agent" : set(),
            "cookies_sent" : set(),
            "anything_else": set()
        }
        """
        self.res = defaultdict(set)        
        self.extension = extension
        self.flow_file = flow_file
        self.fp = self.get_party('first')
        self.tp = self.get_party('third')

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

    def get_leaks(self, payloads) -> dict:
        """
        returns:
        {
           "domain_of_page": bool,
            "page_content": bool,
            "google_search_results": bool,
            ...
        }
        """
        pass

    # def get_payloads(self, endpoint):
    #     payloads = []
    #     try:
    #         with open(self.flow_file, "rb") as f:
    #             reader = FlowReader(f)
    #             for flow in reader.stream():
    #                 if not isinstance(flow, HTTPFlow):
    #                     continue

    #                 if endpoint not in flow.request.url:
    #                     continue

    #                 try:
    #                     request_data = json.loads(flow.request.content.decode('utf-8'))
    #                     payloads.append(request_data)
    #                 except (json.JSONDecodeError, UnicodeDecodeError):
    #                     pass
    #     except Exception as e:
    #         print(e)
    #     return payloads

    def get_summary(self, endpoints: list[str]):
        all_payloads = []
        for url in endpoints:
            all_payloads.append(self.get_payloads(url))
        return self.get_leaks()

    def run(self):
        first_parties = self.get_party('first')
        fp_summary = self.get_summary(first_parties)

        third_parties = self.get_party('third')
        tp_summary = self.get_summary(third_parties)

        return {
            'first-party':fp_summary,
            'third-party': tp_summary
        }

    def get_all_payloads(self, endpoint):
        request_payloads = []
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


def main():
    df = pd.read_csv('src/harpa.csv')
    na = networkAnalyzer(df, 'Harpa/harpa-lin-search-new.flow', "Harpa")
    all_payloads = na.get_all_payloads("api.harpa.ai/api/v1/ai/")
    # with open('all_payloads.json', 'w') as f:
    #     json.dump(all_payloads, f, indent=2)

if __name__ == "__main__":
   main()


"""
TODO: 
1. get mitmproxy package to work
2. look in to the mitmfile structure and remove noise
3. get_leaks a bit more involved so dont stress for now
"""