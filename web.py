from fastapi import FastAPI
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from api.api_openrouter_client import chat_stream
from core.corebrain import ask_jarvis
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def home():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()


@app.post("/chat")
async def chat(request: dict):
    user_input = request["message"]

    # Строим сообщения так же, как в терминальной версии
    answer = ask_jarvis(user_input)

    return {"response": answer}