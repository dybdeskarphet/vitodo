from rich.console import Console
from vitodo.logger import error
from vitodo.messages import ErrorMessages
from vitodo.types import Priority, TabularMatch, TodoItem
from rich.table import Table
from rich import box


class Visualizer:
    def __init__(self, todo_items: list[TodoItem]):
        self.todo_items = todo_items
        self.todo_items_grouped: dict[str, list[TodoItem]] = {}

    def _handle_priority_item_grouping(self, key: Priority, item: TodoItem):
        print(item)
        if key.name in self.todo_items_grouped:
            self.todo_items_grouped[key.name].append(item)
        else:
            self.todo_items_grouped[key.name] = [item]

    def _handle_list_item_grouping(self, keys: list[str], item: TodoItem):
        for key in keys:
            if key in self.todo_items_grouped:
                self.todo_items_grouped[key].append(item)
            else:
                self.todo_items_grouped[key] = [item]

    def group_by(self, key: TabularMatch):
        for item in self.todo_items:
            try:
                item_desc = item.get("description")
                item_key = item.get(key)
                if not item_desc or not item_key:
                    error(ErrorMessages.NO_ITEM_PROPERTIES_GROUPING.value)
                    exit(1)

                if isinstance(item_key, Priority):
                    self._handle_priority_item_grouping(item_key, item)
                elif isinstance(item_key, list):
                    self._handle_list_item_grouping(item_key, item)

            except KeyError as e:
                error(f"{ErrorMessages.GROUP_BY_KEY_ERROR.value} {e}")
                exit(1)
            except Exception as e:
                error(f"{ErrorMessages.INTERNAL_ERROR.value} {e}")
                exit(1)

    def generate_table(self):
        for key, values in self.todo_items_grouped.items():
            console = Console(width=60)
            table = Table(box=box.MINIMAL)
            table.add_column("start")
            table.add_column(key, no_wrap=False)
            for value in values:
                table.add_row(
                    value.get("start_date").strftime("%m/%d/%Y"),
                    value.get("description"),
                )
            console.print(table)
