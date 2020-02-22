import argparse
from argparse import Namespace
from typing import Any, NamedTuple, Optional, Sequence

Argument = NamedTuple("Argument", (("names", Optional[Sequence[str]]), ("default", Any), ("help", Optional[str])))
Argument.__new__.__defaults__ = (None, ..., None)


class FullArgumentData:
    def __init__(self, names: Sequence[str], default: Any, help_message: Optional[str] = None):
        self.names = names
        self.default = default
        self.help_message = help_message

    @property
    def is_required(self) -> bool:
        return self.default is ...

    @classmethod
    def from_raw_data(cls, var_name: str, default: Any) -> "FullArgumentData":
        cli_name = var_name_to_arg_name(var_name)
        return cls(names=[cli_name], default=default)

    @classmethod
    def from_user_arg_data(cls, var_name: str, arg_data: Argument) -> "FullArgumentData":
        cli_names = [var_name_to_arg_name(var_name)] if arg_data.names is None else arg_data.names
        return cls(names=cli_names, default=arg_data.default, help_message=arg_data.help)


def get_cmd_line_args(args: Sequence[FullArgumentData]) -> Namespace:
    parser = argparse.ArgumentParser(allow_abbrev=False)

    for arg in args:
        parser.add_argument(*arg.names, default=arg.default, required=arg.is_required, help=arg.help_message)

    return parser.parse_args()


def var_name_to_arg_name(arg_name: str) -> str:
    formatted_arg_name = arg_name.replace("_", "-")
    return f"--{formatted_arg_name}"


def get_arg_value_from_namespace(cli_arg_names: Sequence[str], namespace: Namespace) -> str:
    multi_dash_names = [name for name in cli_arg_names if name.startswith("--")]
    cli_arg_name = multi_dash_names[0] if multi_dash_names else cli_arg_names[0]
    namespace_field_name = cli_arg_name.lstrip("-").replace("-", "_")
    return namespace.__getattribute__(namespace_field_name)
