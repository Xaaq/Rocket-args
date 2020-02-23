from typing import List

import pytest
from _pytest.capture import CaptureFixture

from rocket_args import Argument
from rocket_args.main import RocketBase
from tests.utils import patch_cli_args


class TestParseArgs:
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

    # noinspection PyUnresolvedReferences
    @staticmethod
    def test_not_provided_required_arguments_display_appropriate_message(capsys: CaptureFixture) -> None:
        class Args(RocketBase):
            arg_1: str = Argument(names=["-a1", "--arg-1", "----long-arg-1"])
            arg_2: str = Argument(names=["-a2", "--arg-2", "----long-arg-2"])

        with patch_cli_args([]), pytest.raises(SystemExit):
            Args.parse_args()

        output = capsys.readouterr().err
        assert "the following arguments are required" in output

        for argument in [Args.arg_1, Args.arg_2]:
            names = "/".join(argument.names)
            assert names in output

    @staticmethod
    def test_not_provided_arguments_with_direct_defaults_set_fallback_to_them() -> None:
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
    def test_not_provided_arguments_with_indirect_defaults_set_fallback_to_them() -> None:
        class Args(RocketBase):
            arg_int: int = Argument(default=123)
            arg_str: str = Argument(default="abc")
            arg_float: float = Argument(default=123.456)

        with patch_cli_args([]):
            output_args = Args.parse_args()

        assert output_args.arg_int == 123
        assert output_args.arg_str == "abc"
        assert output_args.arg_float == 123.456

    @staticmethod
    @pytest.mark.parametrize(
        "cli_args",
        [["-a", "value"], ["--arg", "value"], ["----long-arg-name", "value"]],
        ids=["short arg", "long arg", "very long args"],
    )
    def test_all_arg_names_can_be_provided_from_cli(cli_args: List[str]) -> None:
        class Args(RocketBase):
            arg: str = Argument(names=["-a", "--arg", "----long-arg-name"])

        with patch_cli_args(cli_args):
            output_args = Args.parse_args()

        assert output_args.arg == "value"

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

    # noinspection PyUnresolvedReferences
    @staticmethod
    def test_help_message_contains_arguments_data(capsys: CaptureFixture) -> None:
        class Args(RocketBase):
            arg_1: str = Argument(names=["-a1", "--arg-1"], help="First argument.")
            arg_2: str = Argument(names=["-a2", "--arg-2"], help="Second argument.")

        cli_args = ["--help"]

        with patch_cli_args(cli_args), pytest.raises(SystemExit):
            Args.parse_args()

        output = capsys.readouterr().out

        for argument in [Args.arg_1, Args.arg_2]:
            for name in argument.names:
                assert name in output
            assert argument.help in output


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
