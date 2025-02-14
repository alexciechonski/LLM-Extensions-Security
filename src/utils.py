import ollama
import json
def json_size():
    pass

def get_base_prompt(path):
    with open(path, 'r') as f:
        return f.read()

def llm_analysis(prompt):
    try:
        response = ollama.chat(model='llama3:8b-text-q2_K', messages=[{"role": "user", "content": prompt}])
        return response['message']['content']  # Extract the generated response
    except Exception as e:
        return f"Error communicating with Ollama: {e}"

if __name__ == "__main__":
    with open('all_payloads.json', 'r') as f:
        payload = json.load(f)[0]

    meta = """Answer Yes or No to the following questions based on the json. If unsure say NO.
                1. can you see a url of webpage in the json
                2. can you see content of a webpage in the json
                3. can you see Google Search results in the json
            Remeber, I only need yes or no
            """
    print(llm_analysis(meta+str(payload)))
        