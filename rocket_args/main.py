from typing import Any, Dict, List, Sequence, Type, TypeVar

from rocket_args.arg_parsing import get_cmd_line_args, get_env_args
from rocket_args.utils import Argument, Field

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
        fields_data = cls.__get_fields_data()
        parsed_args = cls.__parse_args(fields_data)

        absent_args = [field.name for field in fields_data if field.name not in parsed_args]
        if absent_args:
            joined_args = ", ".join(absent_args)
            print(f"Required args: {joined_args}")
            raise SystemExit(2)

        return cls(**parsed_args)

    @classmethod
    def __get_fields_data(cls) -> List[Field]:
        field_names_with_types = cls.__annotations__
        defaults = [cls.__dict__.get(name, ...) for name in field_names_with_types.keys()]
        args = [Argument(default=default) if not isinstance(default, Argument) else default for default in defaults]
        fields = [
            Field(arg_name, arg_type, arg_data)
            for (arg_name, arg_type), arg_data in zip(field_names_with_types.items(), args)
        ]
        return fields

    @classmethod
    def __parse_args(cls, fields_data: Sequence[Field]) -> Dict[str, Any]:
        defaults = {field.name: field.value.default for field in fields_data if field.value.default is not ...}
        parsed_args = [defaults, get_env_args(fields_data), get_cmd_line_args(fields_data)]
        joined_args = {key: value for args in parsed_args for key, value in args.items()}
        return joined_args
