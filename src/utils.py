import ollama
import json
def json_size():
    pass

def get_base_prompt(path):
    with open(path, 'r') as f:
        return f.read()

def llm_analysis(prompt):
    try:
        response = ollama.chat(model='tinyllama', messages=[{"role": "user", "content": prompt}])
        return response['message']['content']  # Extract the generated response
    except Exception as e:
        return f"Error communicating with Ollama: {e}"

if __name__ == "__main__":
    with open('combined_payload.json', 'r') as f:
        payload = json.load(f)

    questions = ["Can you see my name", "Can you see my location", "Can you see my browsing history", "Can you see my timezone", "Can you the content of a webpage"]

    for q in questions:
        print(llm_analysis(q + "in the payload:" + str(payload)))
        