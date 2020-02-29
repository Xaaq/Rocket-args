import argparse
from argparse import Namespace
from typing import Any, NamedTuple, Optional, Sequence

FullArgumentData = NamedTuple(
    "FullArgumentData", (("names", Sequence[str]), ("default", Any), ("is_required", bool), ("help", Optional[str]))
)


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
