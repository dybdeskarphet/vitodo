from datetime import date
from enum import Enum, auto
from typing import Literal, TypedDict
from pydantic import BaseModel, Field

type TabularMatch = Literal["priority", "context", "project"]
type ColumnMatch = Literal[
    "priority", "start_date", "description", "project", "context", "due_date"
]
type TabularMatchTypes = str | list[str]


class GeneralConfig(BaseModel):
    todo_path: str


class VisualConfig(BaseModel):
    clean_description: bool = False
    date_format: str = "%Y-%m-%d"


class TableConfig(BaseModel):
    group_by: TabularMatch = "priority"
    columns: list[ColumnMatch] = ["description"]


class ConfigModel(BaseModel):
    general: GeneralConfig
    visual: VisualConfig = Field(default_factory=VisualConfig)
    tables: TableConfig = Field(default_factory=TableConfig)


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


type TodoItemProperty = Priority | str | list[str] | date
