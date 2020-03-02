from typing import Any, NamedTuple, Optional, Sequence, Union

Field = NamedTuple("Field", (("name", str), ("type", Any)))


class Argument:
    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        cli_names: Union[bool, Sequence[str]] = True,
        env_name: Union[bool, str] = True,
        default: Any = ...,
        help: Optional[str] = None,
    ):
        self.cli_names = cli_names
        self.env_name = env_name
        self.default = default
        self.help = help
