from datetime import datetime
from vitodo.types import ConfigModel, Priority, TodoItem
from vitodo.logger import error
from re import compile as recmp
from re import sub as resub


class Parser:
    def __init__(self, config: ConfigModel) -> None:
        self._todo_items: list[TodoItem] = []
        self._todo_path = config.general.todo_path
        self._re = {
            "priority": recmp(r"^\(([A-Z])\)"),
            "date": recmp(r"^\d{4}-\d{2}-\d{2}"),
            "context": recmp(r"\@(\S+)"),
            "project": recmp(r"\+(\S+)"),
            "due_date": recmp(r"due:(\S+)"),
        }
        self._clean_desc = config.visual.clean_description

    def _parse_item(self, item: str) -> TodoItem:
        raw_item = item.strip()
        todo_item: TodoItem = {}

        priority_match = self._re["priority"].match(raw_item)
        if priority_match:
            todo_item["priority"] = Priority[priority_match.group(1)]
            raw_item = resub(self._re["priority"], "", raw_item).strip()
        else:
            todo_item["priority"] = "no priority"

        date_match = self._re["date"].match(raw_item)
        if date_match:
            todo_item["start_date"] = datetime.strptime(date_match.group(), "%Y-%m-%d")
            raw_item = resub(self._re["date"], "", raw_item).strip()
        else:
            todo_item["start_date"] = "unknown"

        context_match = self._re["context"].findall(raw_item)
        if context_match:
            todo_item["context"] = context_match
            raw_item = (
                resub(self._re["context"], "", raw_item).strip()
                if self._clean_desc
                else raw_item
            )
        else:
            todo_item["context"] = "no context"

        project_match = self._re["project"].findall(raw_item)
        if project_match:
            todo_item["project"] = project_match
            raw_item = (
                resub(self._re["project"], "", raw_item).strip()
                if self._clean_desc
                else raw_item
            )
        else:
            todo_item["project"] = "no project"

        due_match = self._re["due_date"].search(raw_item)
        if due_match:
            todo_item["due_date"] = datetime.strptime(due_match.group(1), "%Y-%m-%d")
            raw_item = resub(self._re["due_date"], "", raw_item).strip()
        else:
            todo_item["due_date"] = "indefinite"

        raw_item = resub(r"(\+|\@)", "", raw_item)
        raw_item = resub(r" +", " ", raw_item)
        todo_item["description"] = raw_item

        return todo_item

    def parse_todo_list(self):
        try:
            with open(self._todo_path, "r") as file:
                for line in file:
                    self._todo_items.append(self._parse_item(line))
        except OSError as err:
            error(f"OS error: {err}")
            exit(1)
        except Exception as err:
            error(f"Unexpected {err=}, {type(err)=}")
            exit(1)

        return self._todo_items
