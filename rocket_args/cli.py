import argparse
from argparse import Namespace
from typing import Any, Dict, Optional, Sequence

from rocket_args.utils import Argument, FieldData


def get_cli_args(field_to_arg: Dict[FieldData, Argument]) -> Dict[str, Any]:
    cli_names = [
        arg.cli_names if arg.cli_names else [var_name_to_arg_name(field.name)] for field, arg in field_to_arg.items()
    ]
    cli_args_data = [
        FullArgumentData(names=names, default=..., is_required=arg.default is ..., help=arg.help)
        for names, arg in zip(cli_names, field_to_arg.values())
    ]

    namespace = get_cmd_line_args(cli_args_data)

    cli_values = [get_arg_from_namespace(namespace, arg.names) for arg in cli_args_data]
    name_to_value = {
        field.name: field.type(cli_value)
        for field, cli_value in zip(field_to_arg.keys(), cli_values)
        if cli_value is not ...
    }
    return name_to_value


class FullArgumentData:
    # noinspection PyShadowingBuiltins

    def __init__(self, names: Sequence[str], default: Any, is_required: bool, help: Optional[str]):
        self.names = names
        self.default = default
        self.is_required = is_required
        self.help = help


def var_name_to_arg_name(arg_name: str) -> str:
    formatted_arg_name = arg_name.replace("_", "-")
    return f"--{formatted_arg_name}"


def get_cmd_line_args(args: Sequence[FullArgumentData]) -> Namespace:
    parser = argparse.ArgumentParser(allow_abbrev=False)

    for arg in args:
        parser.add_argument(*arg.names, default=arg.default, required=arg.is_required, help=arg.help)

    return parser.parse_args()


def get_arg_from_namespace(namespace: Namespace, cli_arg_names: Sequence[str]) -> str:
    multi_dash_names = [name for name in cli_arg_names if name.startswith("--")]
    cli_arg_name = multi_dash_names[0] if multi_dash_names else cli_arg_names[0]
    namespace_field_name = cli_arg_name.lstrip("-").replace("-", "_")
    return namespace.__getattribute__(namespace_field_name)
