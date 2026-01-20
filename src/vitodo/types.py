from pydantic import BaseModel
from pathlib import Path

class GeneralConfig(BaseModel):
    todo_path: Path = Path()


class ConfigModel(BaseModel):
    general: GeneralConfig
