def get_all_values(nested_dict):
    values = []

    def extract_values(d):
        for key, value in d.items():
            if isinstance(value, dict):
                extract_values(value)
            else:
                values.append(value)
    extract_values(nested_dict)
    return values


if __name__ == "__main__":
    import json
    with open('src/harpa_leak.json', 'r') as f:
        j = json.load(f)
    print(get_all_values(j))