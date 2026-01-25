from rich import box
from rich.console import Console
from rich.style import Style
from rich.table import Table
from vitodo.config import config
from vitodo.helpers import todo_property_to_string
from vitodo.logger import error
from vitodo.messages import ErrorMessages
from vitodo.types import (
    BoxType,
    ColumnMatch,
    GroupedViewTodoList,
    Priority,
    TabularMatch,
    TitleStyle,
    TodoItem,
)


class GroupedTodoView:
    """
    `__init__` only initializes the class, you have to use
    `.group(<grouping_method>)` to get the grouped to-do items.
    """

    def __init__(self, todo_list: list[TodoItem], columns: list[ColumnMatch]):
        self._todo_list: list[TodoItem] = todo_list
        self._grouped_todo_list: GroupedViewTodoList = {}
        self._columns: list[ColumnMatch] = columns

    def _handle_priority_item_grouping(self, key: Priority, item: TodoItem):
        column_pack = []
        for c in self._columns:
            column_pack.append(todo_property_to_string(item.get(c)))

        if key.name in self._grouped_todo_list:
            self._grouped_todo_list[key.name].append(tuple(column_pack))
        else:
            self._grouped_todo_list[key.name] = [tuple(column_pack)]

    def _handle_list_item_grouping(self, keys: list[str], item: TodoItem):
        for key in keys:
            column_pack = []
            for c in self._columns:
                column_pack.append(todo_property_to_string(item.get(c)))

            if key in self._grouped_todo_list:
                self._grouped_todo_list[key].append(tuple(column_pack))
            else:
                self._grouped_todo_list[key] = [tuple(column_pack)]

    def get_columns(self) -> list[ColumnMatch]:
        return self._columns

    def group(self, group_by: TabularMatch) -> GroupedViewTodoList:
        for item in self._todo_list:
            item_desc = item.get("description")
            item_key = item.get(group_by)
            if not item_desc or not item_key:
                error(ErrorMessages.NO_ITEM_PROPERTIES_GROUPING.value)
                exit(1)

            if isinstance(item_key, Priority):
                self._handle_priority_item_grouping(item_key, item)
            elif isinstance(item_key, list):
                self._handle_list_item_grouping(item_key, item)

        return self._grouped_todo_list


def render_grouped_view(
    grouped_list: GroupedViewTodoList,
    box_type: BoxType,
    title_style: TitleStyle,
    columns: list[ColumnMatch],
):
    console = Console(width=60)
    for grouping_key, items in grouped_list.items():
        table = Table(
            title=grouping_key,
            box=getattr(box, box_type, box.MINIMAL),
            title_style=Style(
                color=title_style.color,
                bold=title_style.bold,
                italic=title_style.italic,
            ),
        )
        [table.add_column(c) for c in config.tables.columns]
        [table.add_row(*r) for r in items]
        console.print(table)
