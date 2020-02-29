from typing import Any, Type, TypeVar

from rocket_args.cli import get_cli_args
from rocket_args.utils import Argument, FieldData, get_defaults, get_env_args

T = TypeVar("T", bound="RocketBase")


class RocketBase:
    def __init__(self, **data: Any):
        for name, value in data.items():
            self.__setattr__(name, value)

    def __repr__(self) -> str:
        args = [f"{name}={value}" for name, value in self.__dict__.items()]
        concatenated_args = ", ".join(args)
        return f"{self.__class__.__name__}({concatenated_args})"

    @classmethod
    def parse_args(cls: Type[T]) -> T:
        field_names_with_types = cls.__annotations__
        defaults = [cls.__dict__.get(name, ...) for name in field_names_with_types.keys()]
        args = [Argument(default=default) if not isinstance(default, Argument) else default for default in defaults]
        field_to_arg = {
            FieldData(arg_name, arg_type): arg_data
            for (arg_name, arg_type), arg_data in zip(field_names_with_types.items(), args)
        }

        parsed_defaults = get_defaults(field_to_arg)
        parsed_env_args = get_env_args(field_to_arg)
        parsed_cli_args = get_cli_args(field_to_arg)
        joined_args = {**parsed_defaults, **parsed_env_args, **parsed_cli_args}
        return cls(**joined_args)
