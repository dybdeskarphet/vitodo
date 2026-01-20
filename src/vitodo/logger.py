from rich.console import Console

console = Console()
error_console = Console(stderr=True)


def error(msg: str):
    error_console.print(rf"[bold red]\[vitodo][/bold red] {msg}")


def log(msg: str):
    console.print(rf"[bold green]\[vitodo][/bold green] {msg}")


def warn(msg: str):
    console.print(rf"[bold yellow]\[vitodo][/bold yellow] {msg}")
