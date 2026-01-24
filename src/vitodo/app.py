import typer
from vitodo.config import config
from vitodo.parser import Parser
from vitodo.visual import GroupedTodoView, render_grouped_view

app = typer.Typer(
    help="A very practical and minimal todo.txt CLI tool",
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.command()
def grouped_view():
    todo_list = Parser(config).parse_todo_list()
    grouped_view = GroupedTodoView(todo_list).group(config.tables.group_by)
    render_grouped_view(grouped_view)


if __name__ == "__main__":
    app()
