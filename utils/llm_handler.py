import os
import requests
import json

HF_MODEL = "mistralai/Mistral-7B-Instruct-v0.2"

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

# Hugging Face Fallback (Mistral 7B Instruct)
def query_llama_hf(prompt: str, api_key: str) -> str:
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {api_key}"}
    payload = {
        "inputs": f"<s>[INST] {prompt} [/INST]",
        "parameters": {"max_new_tokens": 300, "return_full_text": False}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            if isinstance(result, list) and len(result) > 0 and "generated_text" in result[0]:
                return result[0]["generated_text"]
            else:
                return "HF API Error: Unexpected response format."
        else:
            return f"HF API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"HF API request failed: {e}"

# Unified Handler
def query_llm(prompt: str, use_local=True) -> str:
    if use_local:
        return query_llama_local(prompt)
    else:
        api_key = os.getenv("HF_API_TOKEN", "")
        if not api_key:
            return "HF API token not found in environment variables."
        return query_llama_hf(prompt, api_key)