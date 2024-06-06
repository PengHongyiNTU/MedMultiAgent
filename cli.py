# -*- coding: utf-8 -*-

from typing import AsyncIterator, Dict, Any, Union
import re
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.spinner import Spinner
import asyncio
from loguru import logger
from core import Coordinator


class Entity:
    def __init__(self, prefix: str, console: Console):
        self.prefix = prefix
        self.console = console

    def send_message(self, message: str):
        self.console.print(f"{self.prefix} {message}")


class User(Entity):
    def __init__(self, console: Console):
        super().__init__(":man: [bold cyan]You:[/bold cyan]", console)


class AI(Entity):
    def __init__(self, console: Console):
        super().__init__(":robot: [bold magenta]AI:[/bold magenta]", console)

    async def send_stream_message(self, message_generator: AsyncIterator):
        def create_spinner_panel(stream_message):
            text = f"Status: Generating\n{self.prefix} {stream_message}"
            spinner = Spinner("dots", text=text)
            panel = Panel(
                spinner,
                title="AI Generating Response",
                title_align="left",
                border_style="magenta",
            )
            return panel

        def create_completed_panel(message: str):
            completed_message = (
                f"Status: [green]Completed![/green] \n {self.prefix} {message}"
            )
            panel = Panel(
                completed_message,
                title="AI Generating Response",
                title_align="left",
                border_style="magenta",
            )
            return panel

        typed_message = ""
        with Live(console=self.console, refresh_per_second=10) as live:
            async for char in message_generator:
                typed_message += char
                live.update(create_spinner_panel(typed_message))
            live.update(create_completed_panel(typed_message))


class System(Entity):
    def __init__(self, console: Console):
        super().__init__(":gear: [bold green]System:[/bold green]", console)


class CliApp:
    def __init__(self):
        self.console = Console()
        self.user = User(self.console)
        self.ai = AI(self.console)
        self.system = System(self.console)
        self.coordinator = Coordinator()

    def mainloop(self):
        self.system.send_message("Medical Multi Agent initialized")
        self.system.send_message(
            "Type '/file <file_path>' followed by a url to pass a file to the AI agent",
        )
        self.system.send_message("Type '/bye' to exit the program")

        async def prompt_loop():
            while True:
                self.system.send_message("Enter your questions or commands:")
                message = input(
                    ">>> ",
                ).strip()  # Using plain input to get user input
                self.console.rule()
                self.user.send_message(message)
                if re.search(r"/bye", message, re.IGNORECASE):
                    logger.info("Exiting the program")
                    self.system.send_message("Exiting the program")
                    break
                else:
                    if match := re.search(
                        r"/file (\w+)",
                        message,
                        re.IGNORECASE,
                    ):
                        file_path = match.group(1).strip()
                        self.system.send_message(f"File path: {file_path}")
                        logger.info(f"User upload a file: {file_path}")
                    message_generator = await self.coordinator.start_with(
                        message,
                    )
                    await self.ai.send_stream_message(message_generator)

        asyncio.run(prompt_loop())

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    CliApp().run()
