import pandas as pd    
from collections import defaultdict

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


class networkAnalyzer:
    def __init__(self, csv_path, output_file_path) -> None:
        self.network = pd.read_csv(csv_path)
        self.output_file_path = output_file_path
        self.files = self.get_files()
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
        self.struct = defaultdict(set)
        self.res = {{file: self.struct} for file in self.files}

    def get_files(self) -> list:
        files = set(self.network['filename'].tolist())
        return list(files)

    def remove_noise(self, domains: set):
        # remove requests that have stupid referrers
        pass

    def get_party(self, party, flow_file):
        df = self.network
        df = df[
            (df['contacted_party'] == f'{party}-party')
            & (df['filename'] == flow_file)
        ]
        domains = set(df['request_domain'].tolist())
        return self.remove_noise(domains)

    def get_leaks(self, endpoint, flow_file) -> dict:
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

    def update_res(self, endpoints, file):
        for url in endpoints:
            leaks = self.get_leaks(url, file)
            for leak_type, val in leaks.items():
                if val == 1:
                    self.res[file][leak_type].add(url)

    def run(self):
        for file in self.files:
            first_parties = self.get_party('first', file)
            self.update_res(first_parties, file)

            third_parties = self.get_party('third', file)
            self.update_res(third_parties, file)


def main():
    pass

if __name__ == "__main__":
   main()


"""
TODO: 
1. get mitmproxy package to work
2. look in to the mitmfile structure and remove noise
3. get_leaks a bit more involved so dont stress for now
"""