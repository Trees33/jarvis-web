import os
import requests
import customtkinter as ctk
from dotenv import load_dotenv
from datetime import datetime
from ddgs import DDGS

# ======================
# НАСТРОЙКИ
# ======================

MODEL = "mistralai/mistral-7b-instruct"
AUTO_SEARCH = True

# ======================
# ИНИЦИАЛИЗАЦИЯ
# ======================

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")

if not API_KEY:
    print("❌ API ключ не найден в .env")
    exit()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

conversation_history = [
    {
        "role": "system",
        "content": """Ты продвинутый AI-ассистент Jarvis PRO.
Ты умеешь:
- Отвечать кратко и умно
- Использовать интернет если вопрос о текущих событиях
- Отличать прошлое, настоящее и будущее
- Давать структурированные ответы
"""
    }
]

# ======================
# ФУНКЦИИ
# ======================

def needs_search(text):
    keywords = [
        "сейчас", "курс", "сегодня", "новости",
        "в данный момент", "цена", "кто сейчас",
        "погода", "президент"
    ]
    return any(word in text.lower() for word in keywords)

def search_web(query):
    results_text = ""
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)
        for r in results:
            results_text += f"{r['title']}\n{r['body']}\n\n"
    return results_text[:4000]

def ask_jarvis(user_input):

    global conversation_history

    if AUTO_SEARCH and needs_search(user_input):
        web_info = search_web(user_input)
        conversation_history.append({
            "role": "system",
            "content": f"Вот актуальная информация из интернета:\n{web_info}"
        })

    conversation_history.append({"role": "user", "content": user_input})

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": MODEL,
            "messages": conversation_history
        }
    )

    if response.status_code != 200:
        return "Ошибка API: " + response.text

    data = response.json()
    answer = data["choices"][0]["message"]["content"]

    conversation_history.append({"role": "assistant", "content": answer})

    return answer


# ======================
# GUI
# ======================

class JarvisApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Jarvis PRO 🤖")
        self.geometry("900x650")

        self.chat_box = ctk.CTkTextbox(self, wrap="word")
        self.chat_box.pack(padx=20, pady=20, fill="both", expand=True)

        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(padx=20, pady=10, fill="x")

        self.entry = ctk.CTkEntry(self.input_frame)
        self.entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        self.entry.bind("<Return>", self.send_message)

        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Отправить",
            command=self.send_message
        )
        self.send_button.pack(side="right")

        self.insert_message("Jarvis PRO запущен 🚀", "assistant")

    def insert_message(self, message, sender):

        time_now = datetime.now().strftime("%H:%M")

        if sender == "user":
            self.chat_box.insert("end", f"\n🟡 Ты [{time_now}]:\n{message}\n")
        else:
            self.chat_box.insert("end", f"\n🤖 Jarvis [{time_now}]:\n{message}\n")

        self.chat_box.see("end")

    def send_message(self, event=None):

        user_text = self.entry.get()

        if not user_text.strip():
            return

        self.insert_message(user_text, "user")
        self.entry.delete(0, "end")

        self.chat_box.update()

        answer = ask_jarvis(user_text)

        self.insert_message(answer, "assistant")


# ======================
# ЗАПУСК
# ======================

if __name__ == "__main__":
    app = JarvisApp()
    app.mainloop()