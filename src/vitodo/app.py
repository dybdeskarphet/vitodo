from typing import Annotated
import typer
from vitodo.config import config
from vitodo.parser import Parser
from vitodo.views.eisenhower import create_eisenhower_matrix, render_eisenhower_matrix
from vitodo.views.grouped import GroupedView, GroupedViewRenderer

app = typer.Typer(
    help="A very practical and minimal todo.txt CLI tool",
    context_settings={"help_option_names": ["-h", "--help"]},
)


GroupTitleArg = Annotated[
    str | None, "Title of the group you want to view (views all not specified)"
]


@app.command(help="Show to-do list grouped with the specified key")
def grouped_view(group: GroupTitleArg = None):
    todo_list = Parser(
        todo_path=config.general.todo_path,
        clean_description=config.visual.clean_description,
    ).parse_todo_list()

    grouped_view = GroupedView(todo_list, config.grouped_view.columns)

    grouped_view_renderer = GroupedViewRenderer(
        grouped_view=grouped_view.group(config.grouped_view.group_by),
        box_type=config.grouped_view.box_type,
        title_style=config.grouped_view.title,
        columns=grouped_view.get_columns(),
        max_column_width=config.grouped_view.max_column_width,
    )

    if group:
        grouped_view_renderer.render_one(
            group, line_separator=config.grouped_view.line_separator
        )
    else:
        grouped_view_renderer.render_all(config.grouped_view.line_separator)


@app.command(help="Show to-do list in an Eisenhower matrix")
def eisenhower_view():
    todo_list = Parser(
        todo_path=config.general.todo_path,
        clean_description=config.visual.clean_description,
    ).parse_todo_list()
    matrix = create_eisenhower_matrix(
        todo_list, config.eisenhower_view.priority_to_field
    )


if __name__ == "__main__":
    app()
