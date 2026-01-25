import typer
from vitodo.config import config
from vitodo.parser import Parser
from vitodo.views.grouped import GroupedView, render_grouped_view

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

    grouped_view = GroupedView(todo_list, config.tables.columns)

    render_grouped_view(
        grouped_list=grouped_view.group(config.tables.group_by),
        box_type=config.tables.box_type,
        title_style=config.tables.title,
        columns=grouped_view.get_columns(),
        max_column_width=config.tables.max_column_width,
    )


if __name__ == "__main__":
    app()
