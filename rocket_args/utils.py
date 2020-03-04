import sys
from enum import Enum
from pathlib import Path
from typing import Any, List, Optional, Sequence, Union


class Argument:
    # noinspection PyShadowingBuiltins
    def __init__(
        self,
        *,
        cli_names: Union[bool, Sequence[str]] = True,
        env_name: Union[bool, str] = True,
        default: Any = ...,
        help: Optional[str] = None,
    ):
        self.cli_names = cli_names
        self.env_name = env_name
        self.default = default
        self.help = help


class Field:
    # noinspection PyShadowingBuiltins
    def __init__(self, name: str, type: Any, value: Argument):
        self.name = name
        self.type = type
        self.value = value

    @property
    def cli_names(self) -> Optional[List[str]]:
        if isinstance(self.value.cli_names, Sequence):
            return list(self.value.cli_names)
        elif self.value.cli_names is True:
            formatted_name = self.name.replace("_", "-")
            return [f"--{formatted_name}"]
        else:
            return None

    @property
    def env_name(self) -> Optional[str]:
        if isinstance(self.value.env_name, str):
            return self.value.env_name
        elif self.value.env_name is True:
            return self.name.upper()
        else:
            return None


class Color(Enum):
    no_color = "\033[0m"
    purple = "\033[1;35m"
    cyan = "\033[1;36m"


class MessageBuilder:
    def __init__(self, fields_data: Sequence[Field]):
        self.__fields_data = fields_data

    def create_help_message(self) -> str:
        program_name = Path(sys.argv[0]).name
        arguments_help = self.__create_arguments_help()
        return f"{program_name} usage:\n{arguments_help}"

    def create_missing_arguments_message(self) -> str:
        arguments_help = self.__create_arguments_help()
        return f"Missing arguments:\n{arguments_help}"

    def __create_arguments_help(self) -> str:
        padding = " " * 2
        help_message = (
            f"{padding}{Color.cyan.value}CLI NAMES\t{Color.purple.value}ENV NAME{Color.no_color.value}\tHELP\n"
        )

        for field in self.__fields_data:
            cli_names = " ".join(field.cli_names) if field.cli_names else ""
            env_name = field.env_name if field.env_name else ""
            arg_help = field.value.help if field.value.help else ""
            help_message += (
                f"{padding}{Color.cyan.value}{cli_names}\t"
                f"{Color.purple.value}{env_name}\t"
                f"{Color.no_color.value}{arg_help}\n"
            )

        return help_message
