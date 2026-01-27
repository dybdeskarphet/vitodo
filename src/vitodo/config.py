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
import tomli_w

from vitodo.messages import ErrorMessages
from vitodo.types import ConfigModel


class Config:
    def __init__(self) -> None:
        self.config_path: Path
        self.app_name: str = "vitodo"
        self.config_raw: dict[str, Any]
        self.config_parsed: ConfigModel
        self._set_config_path()
        self._create_config_if_not_exists()
        self._read_config()
        self._load_config()
        self._expand_config()

    def _create_config_if_not_exists(self):
        config_json = ConfigModel().model_dump()
        if not self.config_path.exists():
            with open(self.config_path, "wb") as f:
                tomli_w.dump(config_json, f)

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
            error(ErrorMessages.NO_HOME.value)
            exit(1)

        config_dir.mkdir(parents=True, exist_ok=True)
        self.config_path = config_dir / "config.toml"

    def _read_config(self):
        try:
            with open(self.config_path, "rb") as f:
                self.config_raw = tomllib.load(f)
        except FileNotFoundError:
            error(f"{ErrorMessages.NO_CONFIG.value}: {self.config_path}")
            exit(1)
        except tomllib.TOMLDecodeError as e:
            error(f"{ErrorMessages.TOML_PARSE_FAILED}: {e}")
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

            error(f"{ErrorMessages.INVALID_CONFIG.value}:")
            console.print(table)
            exit(1)

    def _expand_config(self):
        self.config_parsed.general.todo_path = path.expanduser(
            path.expandvars(self.config_parsed.general.todo_path)
        )


config = Config().config_parsed
