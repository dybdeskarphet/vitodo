from datetime import date
from enum import Enum, auto
from pydantic import BaseModel
from pathlib import Path

from pydantic.dataclasses import dataclass


class GeneralConfig(BaseModel):
    todo_path: Path = Path()


class ConfigModel(BaseModel):
    general: GeneralConfig


class Priority(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()


@dataclass
class TodoItem:
    priority: Priority
    start_date: date
    description: str
    project: str
    context: str
    due_date: date
