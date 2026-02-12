from api.api_openrouter_client import chat
from core.coretools import search_web
from core.corerouter import needs_live_data
from core.corememory import load_memory, save_memory
from config import SYSTEM_PROMPT

memory = load_memory()

def ask_jarvis(user_input):
    global memory

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    messages += memory
    messages.append({"role": "user", "content": user_input})

    if needs_live_data(user_input):
        web_info = search_web(user_input)
        messages.append({
            "role": "system",
            "content": f"Актуальная информация:\n{web_info}"
        })

    answer = chat(messages)

    memory.append({"role": "user", "content": user_input})
    memory.append({"role": "assistant", "content": answer})

    memory = memory[-12:]  # контроль истории
    save_memory(memory)

    return answer