import os
import sys
from typing import Any, Dict, Sequence

from rocket_args.utils import Field


def get_cmd_line_args(fields_data: Sequence[Field]) -> Dict[str, Any]:
    cli_fields_data = [field for field in fields_data if field.value.cli_names]
    cli_args = sys.argv[1:]
    known_args = {}
    unknown_args = []

    while cli_args:
        cli_arg = cli_args.pop(0)

        for field in cli_fields_data:
            if cli_arg in field.cli_names:
                known_args[field.name] = field.type(cli_args.pop(0)) if cli_args else None
                break
        else:
            unknown_args.append(cli_arg)

    if unknown_args:
        unknown_args_str = " ".join(unknown_args)
        raise SystemExit(f"Unknown arguments: {unknown_args_str}")

    return known_args


def get_env_args(fields_data: Sequence[Field]) -> Dict[str, Any]:
    env_fields_data = [field for field in fields_data if field.value.env_name]
    env_names = [
        field.value.env_name if isinstance(field.value.env_name, str) else field.name.upper()
        for field in env_fields_data
    ]
    env_values = [os.environ.get(name, ...) for name in env_names]
    name_to_value = {
        field.name: field.type(value) for field, value in zip(env_fields_data, env_values) if value is not ...
    }
    return name_to_value
