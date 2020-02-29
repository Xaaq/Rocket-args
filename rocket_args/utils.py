from typing import Any, NamedTuple, Optional, Sequence

FieldData = NamedTuple("FieldData", (("name", str), ("type", Any)))


class Argument:
    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        cli_names: Optional[Sequence[str]] = None,
        env_name: Optional[str] = None,
        default: Any = ...,
        help: Optional[str] = None,
    ):
        self.cli_names = cli_names
        self.env_name = env_name
        self.default = default
        self.help = help
