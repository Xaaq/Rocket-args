import pytest
from _pytest.capture import CaptureFixture
from factory import Factory, Sequence
from factory.fuzzy import FuzzyChoice

from rocket_args.utils import ArgData, get_cmd_line_args, var_name_to_arg_name
from tests.utils import patch_cli_args


class ArgDataFactory(Factory):
    class Meta:
        model = ArgData

    name: str = Sequence(lambda i: f"test_arg_{i}")
    is_required: bool = FuzzyChoice((True, False))
    default: str = Sequence(lambda i: f"value_{i}")


def test_provided_arguments_have_appropriate_values() -> None:
    input_args = [ArgDataFactory(name=f"arg_{i}") for i in range(3)]
    cli_args = ["--arg-0", "value_0", "--arg-1", "value_1", "--arg-2", "value_2"]

    with patch_cli_args(cli_args):
        actual_args = get_cmd_line_args(input_args)

    for i in range(3):
        assert actual_args.__getattribute__(f"arg_{i}") == f"value_{i}"


def test_not_provided_required_arguments_display_appropriate_message(capsys: CaptureFixture) -> None:
    input_args = [ArgDataFactory(is_required=True) for _ in range(3)]

    with patch_cli_args([]), pytest.raises(SystemExit):
        get_cmd_line_args(input_args)

    output = capsys.readouterr().err
    assert "the following arguments are required" in output

    for arg_name in input_args:
        cli_arg_name = var_name_to_arg_name(arg_name.name)
        assert cli_arg_name in output


def test_not_provided_not_required_arguments_fallback_to_defaults() -> None:
    input_args = [ArgDataFactory(is_required=False) for _ in range(3)]

    with patch_cli_args([]):
        args = get_cmd_line_args(input_args)

    for arg in input_args:
        assert args.__getattribute__(arg.name) == arg.default


def test_arguments_abbreviations_are_not_allowed(capsys: CaptureFixture) -> None:
    input_args = [ArgDataFactory(name=f"{name}_arg") for name in ("first", "second", "third")]
    cli_args = ["--first", "value", "--second", "value", "--third", "value"]

    with patch_cli_args(cli_args), pytest.raises(SystemExit):
        get_cmd_line_args(input_args)

    capsys.readouterr()
