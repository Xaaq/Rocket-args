import os
from typing import Any, Dict

from rocket_args.utils import Argument, FieldData


def get_env_args(field_to_arg: Dict[FieldData, Argument]) -> Dict[str, Any]:
    env_names = [arg.env_name if arg.env_name else field.name.upper() for field, arg in field_to_arg.items()]
    env_values = [os.environ.get(name, ...) for name in env_names]
    name_to_value = {
        field.name: field.type(env_value)
        for field, env_value in zip(field_to_arg.keys(), env_values)
        if env_value is not ...
    }
    return name_to_value
