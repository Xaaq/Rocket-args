import os
import sys
from typing import Mapping, Optional, Sequence

from rocket_args.utils import Color, Field


def get_cmd_line_args(fields_data: Sequence[Field]) -> Mapping[str, Optional[str]]:
    cli_args = sys.argv[1:]
    known_args = {}
    unknown_args = []

    while cli_args:
        cli_arg = cli_args.pop(0)

        for field in fields_data:
            if field.cli_names and cli_arg in field.cli_names:
                known_args[field.name] = cli_args.pop(0) if cli_args else None
                break
        else:
            unknown_args.append(cli_arg)

    if unknown_args:
        unknown_args_str = " ".join(unknown_args)
        raise SystemExit(f"Unknown arguments: {Color.cli.value}{unknown_args_str}{Color.neutral.value}")

    return known_args


def get_env_args(fields_data: Sequence[Field]) -> Mapping[str, str]:
    field_with_value = [(field, os.environ.get(field.env_name, None)) for field in fields_data if field.env_name]
    name_to_value = {field.name: value for field, value in field_with_value if value is not None}
    return name_to_value

# TODO: change arg_parsing.py -> arg_parsers.py
# TODO: extract fields in tests to factories
