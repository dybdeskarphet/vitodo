from rich import box
from rich.console import Console
from rich.style import Style
from rich.table import Table
from rich.columns import Columns
from vitodo.helpers import todo_property_to_string
from vitodo.logger import error
from vitodo.messages import ErrorMessages
from vitodo.types import (
    BoxType,
    ColumnAndStyleMatch,
    ColumnList,
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

    def __init__(self, todo_list: list[TodoItem], columns: ColumnList):
        self._todo_list: list[TodoItem] = todo_list
        self._grouped_todo_list: GroupedViewTodoList = {}
        self._columns: ColumnList = columns

    def _handle_priority_item_grouping(self, key: Priority, item: TodoItem):
        column_pack = []
        columns = []
        for c in self._columns:
            if isinstance(c, str):
                column_pack.append(todo_property_to_string(item.get(c)))
            else:
                column_pack.append(todo_property_to_string(item.get(c.column)))

        if key.name in self._grouped_todo_list:
            self._grouped_todo_list[key.name].append(tuple(column_pack))
        else:
            self._grouped_todo_list[key.name] = [tuple(column_pack)]

    def _handle_list_item_grouping(self, keys: list[str], item: TodoItem):
        for key in keys:
            column_pack = []
            for c in self._columns:
                if isinstance(c, str):
                    column_pack.append(todo_property_to_string(item.get(c)))
                else:
                    column_pack.append(todo_property_to_string(item.get(c.column)))

            if key in self._grouped_todo_list:
                self._grouped_todo_list[key].append(tuple(column_pack))
            else:
                self._grouped_todo_list[key] = [tuple(column_pack)]

    def get_columns(self) -> ColumnList:
        return self._columns

    def group(self, group_by: TabularMatch) -> GroupedViewTodoList:
        for item in self._todo_list:
            item_key = item.get(group_by)
            if not item_key:
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
    columns: list[ColumnMatch | ColumnAndStyleMatch],
    max_column_width: int,
):
    console = Console()
    group: list[Table] = []
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
        for c in columns:
            if isinstance(c, str):
                table.add_column(c, max_width=max_column_width)
            else:
                table.add_column(
                    c.column,
                    style=Style(bold=c.bold, italic=c.italic, color=c.color),
                    max_width=max_column_width,
                )
        [table.add_row(*r) for r in items]
        group.append(table)

    table_group = Columns(group, equal=True, expand=True)
    console.print(table_group)
