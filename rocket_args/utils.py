import argparse
from argparse import Namespace
from typing import Any, Optional, Sequence


class FullArgumentData:
    # noinspection PyShadowingBuiltins
    def __init__(self, names: Sequence[str], default: Any, help: Optional[str] = None):
        self.names = names
        self.default = default
        self.help = help

    @property
    def is_required(self) -> bool:
        return self.default is ...


class FullArgumentDataFactory:
    # noinspection PyShadowingBuiltins
    def __init__(self, names: Optional[Sequence[str]] = None, default: Any = ..., help: Optional[str] = None):
        self.names = names
        self.default = default
        self.help = help

    def create(self, var_name: str) -> FullArgumentData:
        cli_names = [var_name_to_arg_name(var_name)] if self.names is None else self.names
        return FullArgumentData(names=cli_names, default=self.default, help=self.help)


Argument = FullArgumentDataFactory


def get_cmd_line_args(args: Sequence[FullArgumentData]) -> Namespace:
    parser = argparse.ArgumentParser(allow_abbrev=False)

    for arg in args:
        parser.add_argument(*arg.names, default=arg.default, required=arg.is_required, help=arg.help)

    return parser.parse_args()


def var_name_to_arg_name(arg_name: str) -> str:
    formatted_arg_name = arg_name.replace("_", "-")
    return f"--{formatted_arg_name}"


def get_arg_value_from_namespace(cli_arg_names: Sequence[str], namespace: Namespace) -> str:
    multi_dash_names = [name for name in cli_arg_names if name.startswith("--")]
    cli_arg_name = multi_dash_names[0] if multi_dash_names else cli_arg_names[0]
    namespace_field_name = cli_arg_name.lstrip("-").replace("-", "_")
    return namespace.__getattribute__(namespace_field_name)
