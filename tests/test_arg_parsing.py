from typing import Any, List, Set, Tuple

import pytest

from rocket_args import Argument
from rocket_args.arg_parsing import cast_values, get_cmd_line_args, get_env_args
from rocket_args.utils import Field
from tests.utils import patch_cli_args, patch_env_args


class TestGetCmdLineArgs:
    @staticmethod
    def test_provided_arguments_are_correctly_parsed() -> None:
        fields_data = [
            Field(name="name_1", type=str, value=Argument(cli_names=True)),
            Field(name="name_2", type=int, value=Argument(cli_names=["--arg"])),
            Field(name="name_3", type=float, value=Argument(cli_names=["-a"])),
        ]
        cli_args = ["--name-1", "abcd", "--arg", "1234", "-a", "12.34"]

        with patch_cli_args(cli_args):
            parsed_args = get_cmd_line_args(fields_data)

        expected_args = {"name_1": "abcd", "name_2": "1234", "name_3": "12.34"}
        assert parsed_args == expected_args

    @staticmethod
    def test_turned_off_arguments_arent_gathered_from_command_line() -> None:
        fields_data = [Field(name="name", type=str, value=Argument(cli_names=False))]
        cli_args = ["--name", "abcd"]

        with patch_cli_args(cli_args), pytest.raises(SystemExit):
            get_cmd_line_args(fields_data)

    @staticmethod
    def test_non_existent_arguments_raise_exception_with_informational_message() -> None:
        fields_data = []
        cli_args = ["--arg-1", "abcd", "--arg-2", "1234", "--arg-3", "12.34"]

        with patch_cli_args(cli_args), pytest.raises(SystemExit) as exception:
            get_cmd_line_args(fields_data)

        for arg in cli_args:
            assert arg in str(exception.value)


class TestGetEnvArgs:
    @staticmethod
    def test_provided_arguments_are_correctly_parsed() -> None:
        fields_data = [
            Field(name="name_1", type=str, value=Argument(env_name=True)),
            Field(name="name_2", type=int, value=Argument(env_name="ARG")),
        ]

        with patch_env_args(NAME_1="abcd", ARG="1234"):
            parsed_args = get_env_args(fields_data)

        expected_args = {"name_1": "abcd", "name_2": "1234"}
        assert parsed_args == expected_args

    @staticmethod
    def test_turned_off_arguments_arent_gathered_from_env() -> None:
        fields_data = [Field(name="name", type=str, value=Argument(env_name=False))]

        with patch_env_args(NAME="abcd"):
            parsed_args = get_env_args(fields_data)

        assert parsed_args == {}


# TODO: extract Field creation to factory?
class TestCastValues:
    @staticmethod
    def test_field_type_is_correctly_casted(type_hint: Any, raw_arg: str, parsed_arg: Any) -> None:
        fields = [Field(name="name", type=type_hint, value=Argument())]
        args = {"name": raw_arg}

        actual = cast_values(fields, args)

        expected = {"name": parsed_arg}
        assert actual == expected

    @staticmethod
    def test_argument_not_existing_in_fields_is_let_through() -> None:
        fields = []
        expected = {"name_1": "abcd", "name_2": 1234, "name_3": 12.34}

        actual = cast_values(fields, expected)

        assert actual == expected
