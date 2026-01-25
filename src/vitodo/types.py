from datetime import date
from enum import Enum, auto
from typing import Literal, TypedDict
from pydantic import BaseModel, Field
from rich.color import ColorType

type TabularMatch = Literal["priority", "context", "project"]
type ColumnMatch = Literal[
    "priority", "start_date", "description", "project", "context", "due_date"
]


class ColumnAndStyleMatch(BaseModel):
    column: ColumnMatch = "description"
    color: str = "blue"
    bold: bool = False
    italic: bool = False


type ColumnList = list[ColumnMatch | ColumnAndStyleMatch]


type TabularMatchTypes = str | list[str]
type BoxType = Literal[
    "ASCII",
    "ASCII2",
    "ASCII_DOUBLE_HEAD",
    "SQUARE",
    "SQUARE_DOUBLE_HEAD",
    "MINIMAL",
    "MINIMAL_HEAVY_HEAD",
    "SIMPLE",
    "SIMPLE_HEAD",
    "SIMPLE_HEAVY",
    "HORIZONTALS",
    "ROUNDED",
    "HEAVY",
    "HEAVY_EDGE",
    "HEAVY_HEAD",
    "DOBULE",
    "DOUBLE_EDGE",
    "MARKDOWN",
]
type GroupedViewTodoList = dict[str, list[tuple[str]]]


class GeneralConfig(BaseModel):
    todo_path: str


class VisualConfig(BaseModel):
    clean_description: bool = False
    date_format: str = "%Y-%m-%d"


class TitleStyle(BaseModel):
    color: str = "red"
    bold: bool = True
    italic: bool = False


class TableConfig(BaseModel):
    group_by: TabularMatch = "priority"
    columns: list[ColumnMatch | ColumnAndStyleMatch] = [
        Field(default_factory=ColumnAndStyleMatch)
    ]
    box_type: BoxType = "MINIMAL"
    title: TitleStyle = Field(default_factory=TitleStyle)


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
