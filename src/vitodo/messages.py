from enum import Enum


class ErrorMessages(Enum):
    NO_ITEM_PROPERTIES_GROUPING = (
        "Couldn't find a todo item description or the relevant grouping method"
    )
    GROUP_BY_KEY_ERROR = "Something went wrong while determining the table titles"
    INTERNAL_ERROR = "Internal error"
