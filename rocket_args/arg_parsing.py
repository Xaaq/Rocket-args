import os
import sys
from typing import Any, Dict, Sequence, _GenericAlias

from rocket_args.utils import Color, Field


def get_cmd_line_args(fields_data: Sequence[Field]) -> Dict[str, Any]:
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


def get_env_args(fields_data: Sequence[Field]) -> Dict[str, Any]:
    field_with_value = [(field, os.environ.get(field.env_name, None)) for field in fields_data if field.env_name]
    name_to_value = {field.name: value for field, value in field_with_value if value is not None}
    return name_to_value


def cast_values(fields_data: Sequence[Field], args: Dict[str, str]) -> Dict[str, Any]:
    def cast_value(field_type: Any, value: Any) -> Any:
        if isinstance(field_type, _GenericAlias):
            real_type = field_type.__origin__

            if real_type in (list, tuple, set):
                subtype = field_type.__args__[0]
                divided_arg = [subtype(arg) for arg in value.split(",")]
                return real_type(divided_arg)
            else:
                raise ValueError(f"Type {field_type} is not supported")
        else:
            return field_type(value)

    field_name_to_type = {field.name: field.type for field in fields_data}
    name_to_type_to_value = [(name, field_name_to_type.get(name, None), value) for name, value in args.items()]
    name_to_value = {
        name: value if type_hint is None else cast_value(type_hint, value)
        for name, type_hint, value in name_to_type_to_value
    }
    return name_to_value
