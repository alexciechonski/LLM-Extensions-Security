import pandas as pd    

"""
{'Max.AI-lin-search-new.flow', 'Max.AI-Lin-Summarize.flow', 'Max.AI-Lin-Browse.flow'}
{'Harpa-lin-summarizing.flow', 'Harpa-lin-search-new.flow', 'Harpa-Lin-control.flow', 'Harpa-Lin-browse.flow'}
{'Copilot-lin-control.flow', 'Copilot-lin-summary.flow', 'Copilot-lin-search_new.flow', 'Copilot-lin-browse.flow'}
"""

df = pd.read_csv(
    # "flow_csvs/Max.AI.csv"
    # "flow_csvs/Harpa.csv"
    # "flow_csvs/Copilot.csv"
    'summary.csv'
    )

# filtered_df = df[
#     (df['contacted_party'] == 'third-party')
#     & (df['filename'] == 'Copilot-lin-browse.flow')
#     # & (df['req_header_referer'] != "https://temp-mail.org/")
#     # & (df['req_header_referer'] != "https://chromewebstore.google.com/")
#     ]
# request_domains = filtered_df['request_domain'].tolist()
# rd = set(request_domains)

# print(rd)

df = df[(df['message_type'] == 'file_search_result')]
print(len(df))



