from datetime import date
from vitodo.config import config
from vitodo.types import Priority


def todo_property_to_string(property) -> str:
    if isinstance(property, Priority):
        return property.name
    elif isinstance(property, list):
        return "\n".join(property)
    elif isinstance(property, date):
        return property.strftime(config.visual.date_format)
    else:
        return property
