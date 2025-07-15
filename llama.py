import requests

def ask_llama(prompt: str) -> str:
    try:
        response = requests.post(
            url="http://localhost:11434/api/generate",
            json={"model": "mistral", "prompt": prompt, "stream": False}
        )
        return response.json()["response"]
    except Exception as e:
        return f"❌ AI bilan aloqa xatosi: {e}"
