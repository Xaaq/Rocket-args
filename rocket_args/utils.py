from typing import Any, Dict, NamedTuple, Optional, Sequence


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


FieldData = NamedTuple("FieldData", (("name", str), ("type", Any)))


def get_defaults(field_to_arg: Dict[FieldData, Argument]) -> Dict[str, Any]:
    name_to_value = {field.name: arg.default for field, arg in field_to_arg.items()}
    return name_to_value
