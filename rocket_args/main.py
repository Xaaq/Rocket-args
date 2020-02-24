from typing import Any, Type, TypeVar

from rocket_args.utils import Argument, get_arg_value_from_namespace, get_cmd_line_args

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
        field_names_with_types = cls.__annotations__.items()
        field_names_to_default = {name: cls.__dict__.get(name, ...) for name, _ in field_names_with_types}
        argument_type = type(Argument())
        args = [
            Argument(default=default) if not isinstance(default, argument_type) else default
            for default in field_names_to_default.values()
        ]
        args_with_metadata = [arg(name) for name, arg in zip(field_names_to_default.keys(), args)]

        cmd_line_args = get_cmd_line_args(args_with_metadata)

        parsed_args = {
            arg_name: arg_type(get_arg_value_from_namespace(arg_data.names, cmd_line_args))
            for arg_data, (arg_name, arg_type) in zip(args_with_metadata, field_names_with_types)
        }
        return cls(**parsed_args)
