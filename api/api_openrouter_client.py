import os
import json
import requests
from dotenv import load_dotenv
from config import MODEL, MAX_TOKENS, TEMPERATURE

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")


# Обычный режим (для corebrain / CLI)
def chat(messages):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": messages,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE
        }
    )

    if response.status_code != 200:
        return f"API Error: {response.text}"

    return response.json()["choices"][0]["message"]["content"]


# Стриминг (для веба)
def chat_stream(messages):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": messages,
            "max_tokens": MAX_TOKENS,
            "temperature": TEMPERATURE,
            "stream": True
        },
        stream=True
    )

    for line in response.iter_lines():
        if line:
            decoded = line.decode("utf-8")

            if decoded.startswith("data: "):
                data = decoded.replace("data: ", "")

                if data.strip() == "[DONE]":
                    break

                try:
                    json_data = json.loads(data)
                    delta = json_data["choices"][0]["delta"]

                    if "content" in delta:
                        yield delta["content"]

                except:
                    pass