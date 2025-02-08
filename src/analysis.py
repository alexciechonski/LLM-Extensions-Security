import pandas as pd    
from collections import defaultdict
from flow_processor import FlowProcessor
from mitmproxy.io import FlowReader

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
    # def __init__(self, extension_name, flow_directory, disconnect_json):
    #     super().__init__(extension_name, flow_directory, disconnect_json)
    #     self.network = self.get_dataframe()


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

    def get_leaks(self, endpoint) -> dict:
        """
        returns:
        {
           "domain_of_page": bool,
            "page_content": bool,
            "google_search_results": bool,
            ...
        }
        """
        res = defaultdict(bool)
        print(res)
        with open(self.flow_file, "rb") as file:
            reader = FlowReader(file)            
            for flow in reader.stream():
                if not hasattr(flow, "request") or not flow.request:
                    continue
            
            # page url
            # harpa: url
            # check current url and check vals

            # page_content 
            # harpa: title
            # get html and compare

            # prompt: 
            # harpa messages[i]['user']
            # "scrape prompt" and compare

            # user details

            # device details

            # time of query

            # context text
            # harpa: messages[0]

            # chat history
            # harpa: messages

            # conversation id
            # harpa: space_id

            # user-agent
            # obv

            # cookies
            # obv
            # what cookie means?


            """
            solutions:
                1. use a llm
                    - how to get it to be fast?
                        - scrapegraph
                    - cost of api keys?
                    - cost of server?
                    - not local
                2. "scrape" all data and compare
                    - scraping prompt is difficult
                        - maybe hybrid solution (?)
                    - ethics?
                    - difficult
                3. keywords
                    - can be used as part of the hybrid soluton 
                4. create a simple ml model
                    - might be too hard
            """





            
        


    def update_res(self, endpoints: list[str]):
        for url in endpoints:
            leaks = self.get_leaks(url)
            for leak_type, val in leaks.items():
                if val == 1:
                    self.res[leak_type].add(url)

    def run(self):
        first_parties = self.get_party('first')
        self.update_res(first_parties)

        third_parties = self.get_party('third')
        self.update_res(third_parties)


def main():
    df = pd.read_csv('src/copilot-control.csv')
    na = networkAnalyzer(df, 'Copilot/copilot-lin-control.flow',"copilot")
    print(na.get_leaks(''))

if __name__ == "__main__":
   main()


"""
TODO: 
1. get mitmproxy package to work
2. look in to the mitmfile structure and remove noise
3. get_leaks a bit more involved so dont stress for now
"""