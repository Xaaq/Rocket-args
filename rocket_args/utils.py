import argparse
from argparse import Namespace
from typing import Any, NamedTuple, Sequence

ArgData = NamedTuple("ArgData", (("name", str), ("is_required", bool), ("default", Any)))


def get_cmd_line_args(args: Sequence[ArgData]) -> Namespace:
    parser = argparse.ArgumentParser(allow_abbrev=False)

    for arg in args:
        parser.add_argument(var_name_to_arg_name(arg.name), required=arg.is_required, default=arg.default)

    return parser.parse_args()


def var_name_to_arg_name(arg_name: str) -> str:
    formatted_arg_name = arg_name.replace("_", "-")
    return f"--{formatted_arg_name}"
