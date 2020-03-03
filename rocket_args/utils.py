from typing import Any, List, Optional, Sequence, Union


class Argument:
    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        *,
        cli_names: Union[bool, Sequence[str]] = True,
        env_name: Union[bool, str] = True,
        default: Any = ...,
        help: Optional[str] = None,
    ):
        self.cli_names = cli_names
        self.env_name = env_name
        self.default = default
        self.help = help


class Field:
    # noinspection PyShadowingBuiltins
    def __init__(self, name: str, type: Any, value: Argument):
        self.name = name
        self.type = type
        self.value = value

    @property
    def cli_names(self) -> List[str]:
        if isinstance(self.value.cli_names, list):
            return self.value.cli_names
        else:
            formatted_name = self.name.replace("_", "-")
            return [f"--{formatted_name}"]


class UnknownArguments(Exception):
    pass
