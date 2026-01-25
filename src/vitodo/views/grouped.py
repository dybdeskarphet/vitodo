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
    GroupedViewRows,
    GroupedViewTodoList,
    Priority,
    TabularMatch,
    TitleStyle,
    TodoItem,
)


class GroupedView:
    """
    `__init__` only initializes the class, you have to use
    `.group(<grouping_method>)` to get the grouped to-do items.
    """

    def __init__(self, todo_list: list[TodoItem], columns: ColumnList):
        self._todo_list: list[TodoItem] = todo_list
        self._grouped_todo_list: GroupedViewTodoList = {}
        self._columns: ColumnList = columns

    def _handle_priority_item_grouping(self, key: Priority, item: TodoItem):
        row_pack = []
        for c in self._columns:
            if isinstance(c, str):
                row_pack.append(todo_property_to_string(item.get(c)))
            else:
                row_pack.append(todo_property_to_string(item.get(c.column)))

        if key.name in self._grouped_todo_list:
            self._grouped_todo_list[key.name].append(tuple(row_pack))
        else:
            self._grouped_todo_list[key.name] = [tuple(row_pack)]

    def _handle_list_item_grouping(self, keys: list[str], item: TodoItem):
        for key in keys:
            row_pack = []
            for c in self._columns:
                if isinstance(c, str):
                    row_pack.append(todo_property_to_string(item.get(c)))
                else:
                    row_pack.append(todo_property_to_string(item.get(c.column)))

            if key in self._grouped_todo_list:
                self._grouped_todo_list[key].append(tuple(row_pack))
            else:
                self._grouped_todo_list[key] = [tuple(row_pack)]

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


class GroupedViewRenderer:
    def __init__(
        self,
        grouped_view: GroupedViewTodoList,
        box_type: BoxType,
        title_style: TitleStyle,
        columns: ColumnList,
        max_column_width: int,
    ) -> None:
        self._grouped_view: GroupedViewTodoList = grouped_view
        self._box_type: BoxType = box_type
        self._title_style: TitleStyle = title_style
        self._columns: ColumnList = columns
        self._max_column_width: int = max_column_width
        self._console: Console = Console()

    def _create_tables(self):
        tables: list[Table] = []
        for grouping_title, rows in self._grouped_view.items():
            table = Table(
                title=grouping_title,
                box=getattr(box, self._box_type, box.MINIMAL),
                title_style=Style(
                    color=self._title_style.color,
                    bold=self._title_style.bold,
                    italic=self._title_style.italic,
                ),
            )
            for c in self._columns:
                if isinstance(c, str):
                    table.add_column(c, max_width=self._max_column_width)
                else:
                    table.add_column(
                        c.column,
                        style=Style(bold=c.bold, italic=c.italic, color=c.color),
                        max_width=self._max_column_width,
                    )
            [table.add_row(*r) for r in rows]
            tables.append(table)

        return tables

    def render_all(self):
        tables = self._create_tables()
        self._console.print(Columns(tables, equal=True, expand=True))

    def render_one(self, selected_group_title: str):
        tables = self._create_tables()
        for table in tables:
            if table.title == selected_group_title:
                self._console.print(table)
                break
