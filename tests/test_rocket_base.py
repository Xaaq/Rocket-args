import os
from typing import List

import pytest
from _pytest.capture import CaptureFixture

from rocket_args import Argument
from rocket_args.main import RocketBase
from tests.utils import patch_cli_args


class TestParseArgsWithoutUsingArgument:
    @staticmethod
    def test_provided_arguments_return_appropriate_values() -> None:
        class Args(RocketBase):
            arg_int: int
            arg_str: str
            arg_float: float

        cli_args = ["--arg-int", "123", "--arg-str", "abc", "--arg-float", "123.456"]

        with patch_cli_args(cli_args):
            output_args = Args.parse_args()

        assert output_args.arg_int == 123
        assert output_args.arg_str == "abc"
        assert output_args.arg_float == 123.456

    @staticmethod
    def test_not_provided_arguments_fallback_to_defaults() -> None:
        class Args(RocketBase):
            arg_int: int = 123
            arg_str: str = "abc"
            arg_float: float = 123.456

        with patch_cli_args([]):
            output_args = Args.parse_args()

        assert output_args.arg_int == 123
        assert output_args.arg_str == "abc"
        assert output_args.arg_float == 123.456

    @staticmethod
    def test_not_provided_required_arguments_display_appropriate_message(capsys: CaptureFixture) -> None:
        class Args(RocketBase):
            arg_1: str
            arg_2: str

        with patch_cli_args([]), pytest.raises(SystemExit):
            Args.parse_args()

        output = capsys.readouterr().err
        assert "the following arguments are required" in output
        assert "--arg-1" in output
        assert "--arg-2" in output

    @staticmethod
    def test_help_message_contains_arguments_metadata(capsys: CaptureFixture) -> None:
        class Args(RocketBase):
            arg_1: str
            arg_2: str

        cli_args = ["--help"]

        with patch_cli_args(cli_args), pytest.raises(SystemExit):
            Args.parse_args()

        output = capsys.readouterr().out
        assert "--arg-1" in output
        assert "--arg-2" in output

    @staticmethod
    def test_arguments_abbreviations_are_not_allowed(capsys: CaptureFixture) -> None:
        class Args(RocketBase):
            first_arg: str
            second_arg: str
            third_arg: str

        cli_args = ["--first", "value", "--second", "value", "--third", "value"]

        with patch_cli_args(cli_args), pytest.raises(SystemExit):
            Args.parse_args()

        capsys.readouterr()


class TestParseArgsUsingArgument:
    @staticmethod
    @pytest.mark.parametrize(
        "cli_args",
        [["-a", "value"], ["--arg", "value"], ["----long-arg-name", "value"]],
        ids=["short arg", "long arg", "very long arg"],
    )
    def test_all_arg_names_can_be_provided_from_cli(cli_args: List[str]) -> None:
        class Args(RocketBase):
            arg: str = Argument(names=["-a", "--arg", "----long-arg-name"])

        with patch_cli_args(cli_args):
            output_args = Args.parse_args()

        assert output_args.arg == "value"

    @staticmethod
    def test_not_provided_arguments_fallback_to_defaults() -> None:
        class Args(RocketBase):
            arg_int: int = Argument(default=123)
            arg_str: str = Argument(default="abc")
            arg_float: float = Argument(default=123.456)

        with patch_cli_args([]):
            output_args = Args.parse_args()

        assert output_args.arg_int == 123
        assert output_args.arg_str == "abc"
        assert output_args.arg_float == 123.456

    # noinspection PyUnresolvedReferences
    @staticmethod
    def test_not_provided_required_arguments_display_appropriate_message(capsys: CaptureFixture) -> None:
        names_1 = ["-a1", "--arg-1", "----long-arg-1"]
        names_2 = ["-a2", "--arg-2", "----long-arg-2"]

        class Args(RocketBase):
            arg_1: str = Argument(names=names_1)
            arg_2: str = Argument(names=names_2)

        with patch_cli_args([]), pytest.raises(SystemExit):
            Args.parse_args()

        output = capsys.readouterr().err
        assert "the following arguments are required" in output

        for name_list in [names_1, names_2]:
            names = "/".join(name_list)
            assert names in output

    # noinspection PyUnresolvedReferences
    @staticmethod
    def test_help_message_contains_arguments_metadata(capsys: CaptureFixture) -> None:
        arg_data_1 = dict(names=["-a1", "--arg-1"], help="First argument.")
        arg_data_2 = dict(names=["-a2", "--arg-2"], help="Second argument.")

        class Args(RocketBase):
            arg_1: str = Argument(names=arg_data_1["names"], help=arg_data_1["help"])
            arg_2: str = Argument(names=arg_data_2["names"], help=arg_data_2["help"])

        cli_args = ["--help"]

        with patch_cli_args(cli_args), pytest.raises(SystemExit):
            Args.parse_args()

        output = capsys.readouterr().out

        for argument in [arg_data_1, arg_data_2]:
            for name in argument["names"]:
                assert name in output
            assert argument["help"] in output


class TestParseArgsUsingEnv:
    @staticmethod
    @pytest.mark.skip
    def test_cli_arguments_are_not_generated() -> None:
        class Args(RocketBase):
            arg_1: str = Argument(env="ARG_1")
            arg_2: str = Argument(env="ARG_2")
            arg_3: str = Argument(env="ARG_3")

        value = "value"
        cli_args = ["--arg-1", value, "--arg-2", value, "--arg-3", value]

        with patch_cli_args(cli_args):
            args = Args.parse_args()

        assert args.arg_1 != value
        assert args.arg_2 != value
        assert args.arg_3 != value

    @staticmethod
    @pytest.mark.skip
    def test_provided_env_vars_return_appropriate_values() -> None:
        class Args(RocketBase):
            arg_int: int = Argument(env="ARG_INT")
            arg_float: float = Argument(env="ARG_FLOAT")
            arg_str: str = Argument(env="ARG_STR")

        os.environ["ARG_INT"] = "1234"
        os.environ["ARG_FLOAT"] = "12.34"
        os.environ["ARG_STR"] = "abcd"

        args = Args.parse_args()

        assert args.arg_int == 1234
        assert args.arg_float == 12.34
        assert args.arg_str == "abcd"


class TestRepr:
    @staticmethod
    def test_provided_arguments_are_present() -> None:
        class Args(RocketBase):
            arg_int: int
            arg_str: str
            arg_float: float

        arguments = dict(arg_int=123, arg_str="abc", arg_float=123.456)
        args = str(Args(**arguments))

        for name, value in arguments.items():
            assert f"{name}={value}" in args

    @staticmethod
    def test_not_provided_arguments_are_not_present() -> None:
        class Args(RocketBase):
            arg_int: int
            arg_str: str
            arg_float: float

        arguments = dict(arg_int=123, arg_str="abc", arg_float=123.456)
        args = str(Args())

        for name, value in arguments.items():
            assert name not in args
            assert str(value) not in args
