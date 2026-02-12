async function sendMessage() {
    const input = document.getElementById("messageInput");
    const text = input.value.trim();

    if (!text) return;

    addMessage(text, "user");
    input.value = "";

    const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text })
    });

    const data = await response.json();
    addMessage(data.response, "bot");
}

function addMessage(text, sender = "bot") {
    const chat = document.getElementById("chat");
    const message = document.createElement("div");

    message.classList.add("message", sender);

    if (sender === "user") {
        message.innerHTML = "<strong>Ты:</strong><br>" + text;
    } else {
        message.innerHTML = "<strong>Jarvis:</strong><br>" + text;
    }

    chat.appendChild(message);
    chat.scrollTop = chat.scrollHeight;
}