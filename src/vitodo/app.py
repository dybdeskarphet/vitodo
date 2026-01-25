import typer
from vitodo.config import config
from vitodo.parser import Parser
from vitodo.visual import GroupedTodoView, render_grouped_view

app = typer.Typer(
    help="A very practical and minimal todo.txt CLI tool",
    context_settings={"help_option_names": ["-h", "--help"]},
)


@app.command(help="Show to-do list grouped with the specified key")
def grouped_view():
    todo_list = Parser(
        todo_path=config.general.todo_path,
        clean_description=config.visual.clean_description,
    ).parse_todo_list()
    grouped_view = GroupedTodoView(todo_list, config.tables.columns).group(
        config.tables.group_by
    )
    render_grouped_view(
        grouped_view,
        box_type=config.tables.box_type,
        title_style=config.tables.title,
        columns=config.tables.columns,
    )


if __name__ == "__main__":
    app()
