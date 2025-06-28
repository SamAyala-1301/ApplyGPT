import os
import requests
import json

OPENROUTER_MODEL = "mistralai/mistral-7b-instruct"

# Local LLaMA 3 via Ollama (if enabled)
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

# OpenRouter API for Mistral 7B
def query_llama_openrouter(prompt: str, api_key: str) -> str:
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": OPENROUTER_MODEL,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 300,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result["choices"][0]["message"]["content"].strip()
        else:
            return f"OpenRouter API Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"OpenRouter API request failed: {e}"

# Unified handler for both local + OpenRouter
def query_llm(prompt: str, use_local=True) -> str:
    if use_local:
        return query_llama_local(prompt)
    else:
        try:
            import streamlit as st
            api_key = st.secrets.get("OPENROUTER_API_KEY", "")
        except Exception:
            api_key = os.getenv("OPENROUTER_API_KEY", "")

        if not api_key:
            return "❌ OpenRouter API token not found. Set it in secrets or env."

        return query_llama_openrouter(prompt, api_key)