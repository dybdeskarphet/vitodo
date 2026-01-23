from datetime import date
from rich.console import Console
from rich.style import Style
from vitodo.config import config
from vitodo.logger import error
from vitodo.messages import ErrorMessages
from vitodo.types import Priority, TabularMatch, TodoItem
from rich.table import Table
from rich import box


class Visualizer:
    def __init__(self, todo_items: list[TodoItem]):
        self.todo_items = todo_items
        self.todo_items_grouped: dict[str, list[tuple[str]]] = {}

    def _handle_priority_item_grouping(self, key: Priority, item: TodoItem):
        column_pack = []
        for c in config.tables.columns:
            column_pack.append(self._handle_property_for_rows(item.get(c)))

        if key.name in self.todo_items_grouped:
            self.todo_items_grouped[key.name].append(tuple(column_pack))
        else:
            self.todo_items_grouped[key.name] = [tuple(column_pack)]

    def _handle_list_item_grouping(self, keys: list[str], item: TodoItem):
        for key in keys:
            column_pack = []
            for c in config.tables.columns:
                column_pack.append(self._handle_property_for_rows(item.get(c)))

            if key in self.todo_items_grouped:
                self.todo_items_grouped[key].append(tuple(column_pack))
            else:
                self.todo_items_grouped[key] = [tuple(column_pack)]

    def _handle_property_for_rows(self, property) -> str:
        if isinstance(property, Priority):
            return property.name
        elif isinstance(property, list):
            return "\n".join(property)
        elif isinstance(property, date):
            return property.strftime(config.visual.date_format)
        else:
            return property

    def group_by(self, key: TabularMatch):
        for item in self.todo_items:
            item_desc = item.get("description")
            item_key = item.get(key)
            if not item_desc or not item_key:
                error(ErrorMessages.NO_ITEM_PROPERTIES_GROUPING.value)
                exit(1)

            if isinstance(item_key, Priority):
                self._handle_priority_item_grouping(item_key, item)
            elif isinstance(item_key, list):
                self._handle_list_item_grouping(item_key, item)

    def generate_table(self):
        console = Console(width=60)
        for grouping_key, items in self.todo_items_grouped.items():
            table = Table(
                title=grouping_key,
                box=getattr(box, config.tables.box_type, box.MINIMAL),
                title_style=Style(
                    color=config.tables.title.color,
                    bold=config.tables.title.bold,
                    italic=config.tables.title.italic,
                ),
            )
            [table.add_column(c) for c in config.tables.columns]
            [table.add_row(*r) for r in items]
            console.print(table)
