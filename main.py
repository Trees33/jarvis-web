from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from core.corebrain import ask_jarvis

console = Console()

console.print(Panel("🔥 Jarvis Ultimate PRO запущен", border_style="green"))

while True:
    user_input = console.input("[bold yellow]Ты:[/bold yellow] ")

    if user_input.lower() == "exit":
        break

    answer = ask_jarvis(user_input)

    console.print(Panel(Markdown(answer), title="🤖 Jarvis", border_style="cyan"))