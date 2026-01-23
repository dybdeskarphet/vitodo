from datetime import date
from enum import Enum, auto
from typing import Literal, TypedDict
from pydantic import BaseModel

type TabularMatch = Literal["priority", "context", "project"]
type TabularMatchTypes = str | list[str]


class GeneralConfig(BaseModel):
    todo_path: str = ""
    clean_description: bool = False


class TableConfig(BaseModel):
    group_by: TabularMatch


class ConfigModel(BaseModel):
    general: GeneralConfig
    tables: TableConfig


class Priority(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()


class TodoItem(TypedDict, total=False):
    priority: Priority | str
    start_date: date | str
    description: str
    project: list[str] | str
    context: list[str] | str
    due_date: date | str
