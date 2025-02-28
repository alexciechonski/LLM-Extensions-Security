import pandas as pd
from extension_audit.analysis import NetworkAnalyzer
df = pd.read_csv('copilot_res.csv')

analyzer = NetworkAnalyzer(df, 'copilot-lin-control.flow', 'copilot')
first_parties = analyzer.get_party('first')

df = df[df['contacted_party'] == 'first-party']
fp_hidden_payloads = df['payload'].tolist()
fp_payloads = [analyzer.combine_payloads(analyzer.get_all_payloads(endpoint)) for endpoint in first_parties]
if fp_hidden_payloads:
    fp_payloads.append({'hidden_payloads':fp_hidden_payloads})

print(fp_payloads)
