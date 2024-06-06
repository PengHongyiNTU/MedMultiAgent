import typer
from cli import CliApp
from web import WebApp
from typer import Option
import datetime
from session import state, State
from typing import Literal

entry_point = typer.Typer()
session_id = datetime.datetime.now().strftime("%Y%m%d%H%M%S")


def initialize_session_state(at: Literal["web", "cli"]) -> None:
    global state
    if state is None:
        state = State(at)



@entry_point.command(help="Start the CLI application.")
def cli() -> None:
    initialize_session_state("cli")
    cli_app = CliApp()
    cli_app.run()


@entry_point.command(help="Start the Web application on the specified port.")
def web(
    port: int = Option(
        8000, "--port", "-p", help="Port number for the web application"
    )
) -> None:
    initialize_session_state("web")
    web_app = WebApp(port)
    web_app.start()


if __name__ == "__main__":
    entry_point()
