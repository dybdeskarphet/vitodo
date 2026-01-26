import json

from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from vitodo.types import (
    EHMatrix,
    Priority,
    PriorityFields,
    TodoItem,
)


def create_eisenhower_matrix(
    todo_list: list[TodoItem], priority_to_field: PriorityFields
):

    priority_to_field_hashmap: dict[str, str] = {}

    for field, priorities in priority_to_field.model_dump().items():
        for priority in priorities:
            priority_to_field_hashmap[priority] = field

    matrix: EHMatrix = {
        "important_urgent": [],
        "important_not_urgent": [],
        "not_important_urgent": [],
        "not_important_not_urgent": [],
    }

    for todo_item in todo_list:
        priority = todo_item.get("priority")
        description = todo_item.get("description")

        if not isinstance(priority, Priority):
            continue

        field = priority_to_field_hashmap.get(priority.name)

        if not isinstance(field, str):
            continue

        if field not in matrix:
            continue

        if not isinstance(description, str) or len(description) == 0:
            continue

        matrix[field].append(description)

    return matrix


