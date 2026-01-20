from datetime import date
from enum import Enum, auto
from typing import TypedDict
from pydantic import BaseModel
from pathlib import Path

from pydantic.dataclasses import dataclass


class GeneralConfig(BaseModel):
    todo_path: str = ""


class ConfigModel(BaseModel):
    general: GeneralConfig


class Priority(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()


class TodoItem(TypedDict, total=False):
    priority: Priority
    start_date: date
    description: str
    project: list[str]
    context: list[str]
    due_date: date
