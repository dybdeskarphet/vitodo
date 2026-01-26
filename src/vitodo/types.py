from ctypes import Array
from datetime import date
from enum import Enum, auto
from typing import Literal, TypedDict
from pydantic import BaseModel, Field

type TabularMatch = Literal["priority", "context", "project"]
type ColumnMatch = Literal[
    "priority", "start_date", "description", "project", "context", "due_date"
]


class ColumnAndStyleMatch(BaseModel):
    column: ColumnMatch = "description"
    color: str = "blue"
    bold: bool = False
    italic: bool = False


class Priority(Enum):
    A = auto()
    B = auto()
    C = auto()
    D = auto()
    E = auto()
    F = auto()
    G = auto()
    H = auto()
    I = auto()
    J = auto()
    K = auto()
    L = auto()
    M = auto()
    N = auto()
    O = auto()
    P = auto()
    Q = auto()
    R = auto()
    S = auto()
    T = auto()
    U = auto()
    V = auto()
    W = auto()
    X = auto()
    Y = auto()
    Z = auto()


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
type GroupedViewRows = list[tuple[str]]
type GroupedViewTodoList = dict[str, GroupedViewRows]


class GeneralConfig(BaseModel):
    todo_path: str


class VisualConfig(BaseModel):
    clean_description: bool = False
    date_format: str = "%Y-%m-%d"


class TitleStyle(BaseModel):
    color: str = "green"
    bold: bool = True
    italic: bool = False


class GroupedViewConfig(BaseModel):
    group_by: TabularMatch = "priority"
    columns: list[ColumnMatch | ColumnAndStyleMatch] = ["description"]
    box_type: BoxType = "MINIMAL"
    title: TitleStyle = Field(default_factory=TitleStyle)
    max_column_width: int = 40
    line_separator: bool = True


type PriorityLiteral = Literal[
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]

type FieldLiteral = Literal[
    "important_urgent",
    "important_not_urgent",
    "not_important_urgent",
    "not_important_not_urgent",
]


class PriorityFields(BaseModel):
    important_urgent: list[PriorityLiteral] = [Priority.A.name]
    important_not_urgent: list[PriorityLiteral] = [Priority.B.name]
    not_important_urgent: list[PriorityLiteral] = [Priority.C.name]
    not_important_not_urgent: list[PriorityLiteral] = [Priority.D.name]


class EisenhowerViewConfig(BaseModel):
    priority_to_field: PriorityFields = Field(default_factory=PriorityFields)


class ConfigModel(BaseModel):
    general: GeneralConfig
    visual: VisualConfig = Field(default_factory=VisualConfig)
    grouped_view: GroupedViewConfig = Field(default_factory=GroupedViewConfig)
    eisenhower_view: EisenhowerViewConfig = Field(default_factory=EisenhowerViewConfig)


class TodoItem(TypedDict, total=False):
    priority: Priority | str
    start_date: date | str
    description: str
    project: list[str] | str
    context: list[str] | str
    due_date: date | str


type EHMatrix = dict[str, list[str]]

type TodoItemProperty = Priority | str | list[str] | date
