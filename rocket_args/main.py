import os
from abc import ABC, abstractmethod
from typing import Any, Dict, Type, TypeVar

from rocket_args.cli_utils import FullArgumentData, get_arg_from_namespace, get_cmd_line_args, var_name_to_arg_name
from rocket_args.utils import Argument, FieldData

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

        parsers = [DefaultsParser(), EnvParser(), CliParser()]
        parsed_args = [parser.parse(field_to_arg) for parser in parsers]
        joined_args = {key: value for args in parsed_args for key, value in args.items()}
        return cls(**joined_args)


class Parsable(ABC):
    @staticmethod
    @abstractmethod
    def parse(field_to_arg: Dict[FieldData, Argument]) -> Dict[str, Any]:
        pass


class CliParser(Parsable):
    @staticmethod
    def parse(field_to_arg: Dict[FieldData, Argument]) -> Dict[str, Any]:
        cli_field_to_arg = {field: arg for field, arg in field_to_arg.items() if arg.cli_names}
        cli_names = [
            arg.cli_names if isinstance(arg.cli_names, list) else [var_name_to_arg_name(field.name)]
            for field, arg in cli_field_to_arg.items()
        ]
        cli_args_data = [
            FullArgumentData(names=names, default=..., is_required=arg.default is ..., help=arg.help)
            for names, arg in zip(cli_names, cli_field_to_arg.values())
        ]

        namespace = get_cmd_line_args(cli_args_data)

        cli_values = [get_arg_from_namespace(namespace, arg.names) for arg in cli_args_data]
        name_to_value = {
            field.name: field.type(value)
            for field, value in zip(cli_field_to_arg.keys(), cli_values)
            if value is not ...
        }
        return name_to_value


class EnvParser(Parsable):
    @staticmethod
    def parse(field_to_arg: Dict[FieldData, Argument]) -> Dict[str, Any]:
        env_field_to_arg = {field: arg for field, arg in field_to_arg.items() if arg.env_name}
        env_names = [
            arg.env_name if isinstance(arg.env_name, str) else field.name.upper()
            for field, arg in env_field_to_arg.items()
        ]
        env_values = [os.environ.get(name, ...) for name in env_names]
        name_to_value = {
            field.name: field.type(value)
            for field, value in zip(env_field_to_arg.keys(), env_values)
            if value is not ...
        }
        return name_to_value


class DefaultsParser(Parsable):
    @staticmethod
    def parse(field_to_arg: Dict[FieldData, Argument]) -> Dict[str, Any]:
        name_to_value = {field.name: arg.default for field, arg in field_to_arg.items()}
        return name_to_value
