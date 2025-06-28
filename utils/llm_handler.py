import os
import requests
import json

# Local LLaMA 3 via Ollama
def query_llama_local(prompt: str) -> str:
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt},
            stream=True
        )

        full_output = ""
        for line in response.iter_lines():
            if line:
                json_data = json.loads(line.decode("utf-8"))
                full_output += json_data.get("response", "")
        return full_output.strip()
    except Exception as e:
        return f"Local LLaMA error: {e}"

# Hugging Face Fallback (Meta LLaMA 3 - 8B)
def query_llama_hf(prompt: str, api_key: str) -> str:
    url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {"inputs": prompt}

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()[0]["generated_text"]
        else:
            return f"HF API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"HF API request failed: {e}"

# Unified Handler
def query_llm(prompt: str, use_local=True) -> str:
    if use_local:
        return query_llama_local(prompt)
    else:
        api_key = os.getenv("HF_API_KEY", "")
        return query_llama_hf(prompt, api_key)