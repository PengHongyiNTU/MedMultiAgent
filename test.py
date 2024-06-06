import asyncio
from rich.console import Console
from rich.panel import Panel
from rich.live import Live
from rich.spinner import Spinner

console = Console()

# Async generator to provide text updates with typing effect
async def text_generator():
    base_text = "Loading... "
    for i in range(10):
        for j in range(len(base_text)):
            await asyncio.sleep(0.1)
            yield base_text[:j+1] + f"{i + 1}/10"
        await asyncio.sleep(1)
    completion_text = "Completed!"
    for j in range(len(completion_text)):
        await asyncio.sleep(0.1)
        yield completion_text[:j+1]

# Function to create a dynamic spinner panel with custom text
def create_spinner_panel(text):
    spinner = Spinner("dots", text=text)
    panel = Panel(spinner, title="Spinner Panel")
    return panel

# Async function to display the spinner within a live panel
async def show_spinner_in_panel():
    with Live(console=console, refresh_per_second=10) as live:
        async for text in text_generator():
            live.update(create_spinner_panel(text))

# Run the async function
asyncio.run(show_spinner_in_panel())
