from rich.console import Console
from rich.panel import Panel
from rich.text import Text
import time

# Initialize the Rich Console
console = Console()

def main():
    # Clear the screen (works on Windows)
    import os
    os.system('cls')

    # Print a beautiful, colored panel
    welcome_text = Text("Welcome to the Neural Key Environment.\nVisual interface libraries successfully installed.", justify="center")
    welcome_text.stylize("bold cyan", 0, 36)
    welcome_text.stylize("green", 37, 85)
    
    console.print(Panel(welcome_text, title="[bold yellow]SYSTEM BOOT[/bold yellow]", border_style="blue", expand=False))

    # Show off a dynamic loading spinner
    with console.status("[bold magenta]Testing dynamic loading animations...", spinner="aesthetic"):
        time.sleep(3) # Pretend to do some heavy lifting
        
    console.print("[bold green]✔ UI Test Complete![/bold green]")

if __name__ == "__main__":
    main()
    