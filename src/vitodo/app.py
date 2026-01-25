from typing import Annotated
import typer
from vitodo.config import config
from vitodo.parser import Parser
from vitodo.views import grouped
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

    grouped_view = GroupedView(todo_list, config.tables.columns)

    grouped_view_renderer = GroupedViewRenderer(
        grouped_view=grouped_view.group(config.tables.group_by),
        box_type=config.tables.box_type,
        title_style=config.tables.title,
        columns=grouped_view.get_columns(),
        max_column_width=config.tables.max_column_width,
    )

    if group:
        grouped_view_renderer.render_one(
            group, line_seperator=config.tables.line_separator
        )
    else:
        grouped_view_renderer.render_all(config.tables.line_separator)


if __name__ == "__main__":
    app()
