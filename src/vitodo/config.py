from pathlib import Path
from os import getenv
from typing import Any
from pydantic import ValidationError
from rich import box
from rich.table import Table
from vitodo.logger import error
from vitodo.logger import console
import tomllib
from os import path

from vitodo.types import ConfigModel


class Config:
    def __init__(self) -> None:
        self.config_path: Path
        self.app_name: str = "vitodo"
        self.config_raw: dict[str, Any]
        self.config_parsed: ConfigModel
        self._set_config_path()
        self._read_config()
        self._load_config()
        self._expand_config()

    def _set_config_path(self):
        home = getenv("HOME")
        xdg_config = getenv("XDG_CONFIG_HOME")
        config_dir: None | Path = None

        if home:
            if xdg_config:
                config_dir = Path(xdg_config) / self.app_name
            else:
                config_dir = Path(home) / ".config" / self.app_name
        else:
            error("No home directory found.")
            exit(1)

        config_dir.mkdir(parents=True, exist_ok=True)
        self.config_path = config_dir / "config.toml"

    def _read_config(self):
        try:
            with open(self.config_path, "rb") as f:
                self.config_raw = tomllib.load(f)
        except FileNotFoundError:
            error(f"Config file not found at {self.config_path}")
            exit(1)
        except tomllib.TOMLDecodeError as e:
            error(f"Failed to parse TOML: {e}")
            exit(1)

    def _load_config(self):
        try:
            self.config_parsed = ConfigModel.model_validate(
                self.config_raw, strict=False, extra="forbid"
            )
        except ValidationError as e:
            table = Table("Location", "Message", "Type", box=box.ROUNDED, min_width=80)
            for err in e.errors():
                loc = " -> ".join(str(x) for x in err["loc"])
                table.add_row(loc, err["msg"], err["type"])

            error(f"Invalid config file:")
            console.print(table)
            exit(1)

    def _expand_config(self):
        self.config_parsed.general.todo_path = path.expanduser(
            path.expandvars(self.config_parsed.general.todo_path)
        )


config = Config().config_parsed
