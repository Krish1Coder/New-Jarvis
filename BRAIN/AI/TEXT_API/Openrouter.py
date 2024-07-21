import requests
import json
import os

chat_history = [{"role": "system", "content": "You are Jarvis"}]

def generate(query: str, model: str = "openchat/openchat-7b", max_tokens: int = 8096,
             temperature: float = 0.85, frequency_penalty: float = 0.34, presence_penalty: float = 0.06,
             repetition_penalty: float = 1.0, top_k: int = 0) -> str:
    global chat_history
    chat_history.append({"role": "user", "content": query})

    response = requests.post(
        url="https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['OPENROUTER']}"},
        data=json.dumps({
            "messages": chat_history,
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "frequency_penalty": frequency_penalty,
            "presence_penalty": presence_penalty,
            "repetition_penalty": repetition_penalty,
            "top_k": top_k,
        })
    )

    try:
        generated_text = response.json()["choices"][0]["message"]["content"].strip()
        chat_history.append({"role": "assistant", "content": generated_text})
        return generated_text
    except Exception as e:
        return f"Failed to Get Response\nError: {e}\nResponse: {response.text}"
