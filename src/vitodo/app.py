import typer
from vitodo.config import config
from vitodo.parser import Parser
from vitodo.visual import Visualizer

app = typer.Typer(
    help="A very practical and minimal todo.txt CLI tool",
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.command()
def dothings():
    todo_list = Parser(config).parse_todo_list()
    visualizer = Visualizer(todo_list)
    visualizer.group_by(config.tables.group_by)
    visualizer.generate_table()


if __name__ == "__main__":
    app()
