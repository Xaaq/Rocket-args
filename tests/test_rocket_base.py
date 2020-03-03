from typing import List

import pytest
from _pytest.capture import CaptureFixture

from rocket_args import Argument
from rocket_args.main import RocketBase
from tests.utils import patch_cli_args, patch_env_args


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
    def test_args_have_appropriate_priorities_first_cli_then_env_then_default() -> None:
        class Args(RocketBase):
            arg_1: str = "default_value"
            arg_2: str = "default_value"
            arg_3: str = "default_value"

        with patch_cli_args(["--arg-1", "cli_value"]), patch_env_args(ARG_1="env_value", ARG_2="env_value"):
            args = Args.parse_args()

        assert args.arg_1 == "cli_value"
        assert args.arg_2 == "env_value"
        assert args.arg_3 == "default_value"

    @staticmethod
    @pytest.mark.skip
    def test_not_provided_required_arguments_display_appropriate_message(capsys: CaptureFixture) -> None:
        class Args(RocketBase):
            arg_1: str
            arg_2: str

        with patch_cli_args([]), pytest.raises(SystemExit):
            Args.parse_args()

        output = capsys.readouterr().err
        assert "--arg-1" in output
        assert "--arg-2" in output

    @staticmethod
    @pytest.mark.skip
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


class TestParseArgsUsingArgument:
    @staticmethod
    @pytest.mark.parametrize(
        "cli_args", [["-a", "value"], ["--arg", "value"]], ids=["short arg", "long arg"],
    )
    def test_all_arg_names_can_be_provided_from_cli(cli_args: List[str]) -> None:
        class Args(RocketBase):
            arg: str = Argument(cli_names=["-a", "--arg"])

        with patch_cli_args(cli_args):
            output_args = Args.parse_args()

        assert output_args.arg == "value"

    @staticmethod
    def test_cli_arguments_are_turned_off() -> None:
        class Args(RocketBase):
            arg_int: int = Argument(cli_names=False)
            arg_str: str = Argument(cli_names=False)
            arg_float: float = Argument(cli_names=False)

        cli_args = ["--arg-int", "5678", "--arg-str", "efgh", "--arg-float", "56.78"]

        with patch_cli_args(cli_args), pytest.raises(SystemExit) as message:
            Args.parse_args()

        occurrences = [arg in str(message) for arg in cli_args]
        assert all(occurrences)

    @staticmethod
    def test_env_arguments_are_turned_off() -> None:
        class Args(RocketBase):
            arg_int: int = Argument(env_name=False, default=1234)
            arg_str: str = Argument(env_name=False, default="abcd")
            arg_float: float = Argument(env_name=False, default=12.34)

        with patch_cli_args([]), patch_env_args(ARG_INT="5678", ARG_STR="efgh", ARG_FLOAT="56.78"):
            output_args = Args.parse_args()

        assert output_args.arg_int == 1234
        assert output_args.arg_str == "abcd"
        assert output_args.arg_float == 12.34

    # noinspection PyUnresolvedReferences
    @staticmethod
    @pytest.mark.skip
    def test_not_provided_required_arguments_display_appropriate_message(capsys: CaptureFixture) -> None:
        class Args(RocketBase):
            arg_1: str = Argument(cli_names=["-a1", "--arg-1", "----long-arg-1"])
            arg_2: str = Argument(cli_names=["-a2", "--arg-2", "----long-arg-2"])

        with patch_cli_args([]), pytest.raises(SystemExit):
            Args.parse_args()

        output = capsys.readouterr().err

        for argument in [Args.arg_1, Args.arg_2]:
            names = "/".join(argument.cli_names)
            assert names in output

    # noinspection PyUnresolvedReferences
    @staticmethod
    @pytest.mark.skip
    def test_help_message_contains_arguments_metadata(capsys: CaptureFixture) -> None:
        class Args(RocketBase):
            arg_1: str = Argument(cli_names=["-a1", "--arg-1"], help="First argument.")
            arg_2: str = Argument(cli_names=["-a2", "--arg-2"], help="Second argument.")

        cli_args = ["--help"]

        with patch_cli_args(cli_args), pytest.raises(SystemExit):
            Args.parse_args()

        output = capsys.readouterr().out

        for argument in [Args.arg_1, Args.arg_2]:
            for name in argument.cli_names:
                assert name in output
            assert argument.help in output

    @staticmethod
    def test_provided_env_vars_return_appropriate_values() -> None:
        class Args(RocketBase):
            arg_int: int
            arg_float: float
            arg_str: str

        with patch_cli_args([]), patch_env_args(ARG_INT="1234", ARG_FLOAT="12.34", ARG_STR="abcd"):
            args = Args.parse_args()

        assert args.arg_int == 1234
        assert args.arg_float == 12.34
        assert args.arg_str == "abcd"

    @staticmethod
    def test_env_vars_names_can_be_customized() -> None:
        class Args(RocketBase):
            arg_int: int = Argument(env_name="MY_ARG_INT")
            arg_float: float = Argument(env_name="MY_ARG_FLOAT")
            arg_str: str = Argument(env_name="MY_ARG_STR")

        with patch_cli_args([]), patch_env_args(MY_ARG_INT="1234", MY_ARG_FLOAT="12.34", MY_ARG_STR="abcd"):
            args = Args.parse_args()

        assert args.arg_int == 1234
        assert args.arg_float == 12.34
        assert args.arg_str == "abcd"

    @staticmethod
    def test_args_have_appropriate_priorities_first_cli_then_env_then_default() -> None:
        class Args(RocketBase):
            arg_1: str = Argument(default="default_value")
            arg_2: str = Argument(default="default_value")
            arg_3: str = Argument(default="default_value")

        with patch_cli_args(["--arg-1", "cli_value"]), patch_env_args(ARG_1="env_value", ARG_2="env_value"):
            args = Args.parse_args()

        assert args.arg_1 == "cli_value"
        assert args.arg_2 == "env_value"
        assert args.arg_3 == "default_value"


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
