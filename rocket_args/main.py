from typing import Any, Type, TypeVar

from rocket_args.utils import ArgData, get_cmd_line_args

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
        user_defined_args = cls.__annotations__
        arg_data = [
            ArgData(name=name, is_required=name not in cls.__dict__, default=cls.__dict__.get(name, ...))
            for name in user_defined_args.keys()
        ]
        cmd_line_args = get_cmd_line_args(arg_data)
        parsed_arguments = {
            arg_name: arg_type(cmd_line_args.__getattribute__(arg_name))
            for arg_name, arg_type in user_defined_args.items()
        }

        return cls(**parsed_arguments)
