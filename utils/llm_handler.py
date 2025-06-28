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
def query_llama_hf(prompt: str, hf_token: str) -> str:
    url = f"https://api-inference.huggingface.co/models/{HF_MODEL}"
    headers = {"Authorization": f"Bearer {hf_token}"}
    payload = {
        "inputs": f"<s>[INST] {prompt} [/INST]",
        "parameters": {"max_new_tokens": 300, "return_full_text": False}
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            # Handle if it's a list of dicts
            if isinstance(result, list):
                return result[0].get("generated_text") or result[0].get("text", "⚠️ No response text.")
            elif isinstance(result, dict) and "generated_text" in result:
                return result["generated_text"]
            else:
                return f"⚠️ Unexpected response format: {result}"
        else:
            return f"HF API Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"HF API request failed: {e}"

# Unified Handler
def query_llm(prompt: str, use_local=True) -> str:
    if use_local:
        return query_llama_local(prompt)
    else:
        # First check Streamlit secrets (for Streamlit Cloud)
        try:
            import streamlit as st
            api_key = st.secrets.get("HF_API_KEY", "")
        except Exception:
            api_key = os.getenv("HF_API_KEY", "")

        if not api_key:
            return "❌ HF API token not found. Set it in secrets or env."

        return query_llama_hf(prompt, api_key)