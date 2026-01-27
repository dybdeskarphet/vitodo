from dataclasses import field
import json
from logging import error

from pydantic import fields
from rich.console import Console, Group
from rich.panel import Panel
from rich.layout import Layout
from rich.style import Style
from rich.text import Text
from vitodo.types import (
    EHMatrix,
    FieldEnum,
    Priority,
    Fields,
    RenderableMatrix,
    TodoItem,
)


def create_eisenhower_matrix(todo_list: list[TodoItem], fields_config: Fields):
    priority_to_field_hashmap: dict[str, str] = {}

    for field_name, field_properties in fields_config.model_dump().items():
        priorities = field_properties.get("priorities")
        for priority in priorities:
            priority_to_field_hashmap[priority] = field_name

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

        field_name = priority_to_field_hashmap.get(priority.name)

        if not isinstance(field_name, str):
            continue

        if field_name not in matrix:
            continue

        if not isinstance(description, str) or len(description) == 0:
            continue

        matrix[field_name].append(description)

    return matrix


class EisenhowerMatrixRenderer:
    def __init__(self, fields_config: Fields, field_size: int) -> None:
        self._console: Console = Console(height=field_size * 2, width=field_size * 4)
        self._field_size: int = field_size
        self._panels: list[Panel] = []
        self._fields_config: Fields = fields_config
        self._renderable_matrix: RenderableMatrix = {
            "important_urgent": {
                "style": Style(
                    color=fields_config.important_urgent.style.color,
                    bold=fields_config.important_urgent.style.bold,
                    italic=fields_config.important_urgent.style.italic,
                ),
                "item_list": Group(),
            },
            "important_not_urgent": {
                "style": Style(
                    color=fields_config.important_not_urgent.style.color,
                    bold=fields_config.important_not_urgent.style.bold,
                    italic=fields_config.important_not_urgent.style.italic,
                ),
                "item_list": Group(),
            },
            "not_important_urgent": {
                "style": Style(
                    color=fields_config.not_important_urgent.style.color,
                    bold=fields_config.not_important_urgent.style.bold,
                    italic=fields_config.not_important_urgent.style.italic,
                ),
                "item_list": Group(),
            },
            "not_important_not_urgent": {
                "style": Style(
                    color=fields_config.not_important_not_urgent.style.color,
                    bold=fields_config.not_important_not_urgent.style.bold,
                    italic=fields_config.not_important_not_urgent.style.italic,
                ),
                "item_list": Group(),
            },
        }

    def populate(self, matrix: EHMatrix):
        for field_name, field_items in matrix.items():
            texts = tuple(
                [Text.assemble("• ", (item, "white")) for item in field_items]
            )
            self._renderable_matrix[field_name]["item_list"] = Group(*texts)

        for field_title, renderable_field in self._renderable_matrix.items():
            self._panels.append(
                Panel(
                    renderable_field.get("item_list"),
                    title=getattr(
                        FieldEnum, field_title, "not_important_not_urgent"
                    ).value,
                    style=renderable_field.get("style"),
                )
            )

        return self

    def render(self):
        layout = Layout(size=self._field_size)
        layout.split_column(
            Layout(size=self._field_size, name="upper"),
            Layout(size=self._field_size, name="lower"),
        )
        layout["upper"].split_row(
            Layout(self._panels[0], name="left", size=self._field_size * 2),
            Layout(self._panels[1], name="right", size=self._field_size * 2),
        )
        layout["lower"].split_row(
            Layout(self._panels[2], name="left", size=self._field_size * 2),
            Layout(self._panels[3], name="right", size=self._field_size * 2),
        )
        self._console.print(layout)
