import os
from typing import Any, Dict, NamedTuple, Optional, Sequence

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


def get_env_args(field_to_arg: Dict[FieldData, Argument]) -> Dict[str, Any]:
    env_names = [arg.env_name if arg.env_name else field.name.upper() for field, arg in field_to_arg.items()]
    env_values = [os.environ.get(name, ...) for name in env_names]
    name_to_value = {
        field.name: field.type(env_value)
        for field, env_value in zip(field_to_arg.keys(), env_values)
        if env_value is not ...
    }
    return name_to_value


def get_defaults(field_to_arg: Dict[FieldData, Argument]) -> Dict[str, Any]:
    name_to_value = {field.name: arg.default for field, arg in field_to_arg.items()}
    return name_to_value
