from pydoc import describe
from typing import Any
from vitodo.logger import console, error
from vitodo.parser import Parser
from vitodo.types import TabularMatch, TodoItem
from rich.table import Table


class Visualizer:
    def __init__(self, todo_items: list[TodoItem]):
        self.todo_items = todo_items

    def group_by(self, key: TabularMatch):
        items_grouped: dict[Any, list[str]] = {}
        for item in self.todo_items:
            try:
                item_desc = item.get("description")
                item_key = item.get(key)
                if item_key and item_desc:
                    if item_key in items_grouped:
                        items_grouped[item_key].append(item_desc)
                    else:
                        items_grouped[item_key] = [item_desc]
            except KeyError:
                error(f"Couldn't find the relevant values of a to-do item.")
                exit(1)
            except Exception as e:
                error(f"Couldn't find the relevant values of a to-do item.")
                exit(1)

        print(items_grouped)


parser = Parser()
vis = Visualizer(parser.todo_items).show_table("priority")
