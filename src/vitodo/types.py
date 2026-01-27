from datetime import date
from enum import Enum, auto
from typing import Literal, TypedDict
from pydantic import BaseModel, Field
from rich.console import Group
from rich.style import Style
from rich.text import Text

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
    todo_path: str = "~/Documents/todo.txt"


class VisualConfig(BaseModel):
    clean_description: bool = False
    date_format: str = "%Y-%m-%d"


class TextStyle(BaseModel):
    color: str = "green"
    bold: bool = False
    italic: bool = False


class GroupedViewConfig(BaseModel):
    group_by: TabularMatch = "priority"
    columns: list[ColumnMatch | ColumnAndStyleMatch] = ["description"]
    box_type: BoxType = "MINIMAL"
    title: TextStyle = Field(default_factory=TextStyle)
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


class FieldEnum(Enum):
    important_urgent = "important, urgent"
    important_not_urgent = "important, not urgent"
    not_important_urgent = "not important, urgent"
    not_important_not_urgent = "not important, not urgent"


class FieldModel(BaseModel):
    style: TextStyle
    priorities: list[PriorityLiteral]


class Fields(BaseModel):
    important_urgent: FieldModel = FieldModel(
        style=TextStyle(color="green"), priorities=[Priority.A.name]
    )
    important_not_urgent: FieldModel = FieldModel(
        style=TextStyle(color="blue"), priorities=[Priority.B.name]
    )
    not_important_urgent: FieldModel = FieldModel(
        style=TextStyle(color="red"), priorities=[Priority.C.name]
    )
    not_important_not_urgent: FieldModel = FieldModel(
        style=TextStyle(color="magenta"), priorities=[Priority.D.name]
    )


class EisenhowerViewConfig(BaseModel):
    fields: Fields = Field(default_factory=Fields)
    field_size: int = 20


class ConfigModel(BaseModel):
    general: GeneralConfig = Field(default_factory=GeneralConfig)
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


class RenderableField(TypedDict):
    style: Style
    item_list: Group


class RenderableMatrix(TypedDict):
    important_urgent: RenderableField
    important_not_urgent: RenderableField
    not_important_urgent: RenderableField
    not_important_not_urgent: RenderableField


type TodoItemProperty = Priority | str | list[str] | date
