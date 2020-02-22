import pytest
from _pytest.capture import CaptureFixture
from factory import Factory, Sequence

from rocket_args.utils import FullArgumentData, get_arg_value_from_namespace, get_cmd_line_args
from tests.utils import patch_cli_args


class FullArgumentDataFactory(Factory):
    class Meta:
        model = FullArgumentData

    names: str = Sequence(lambda i: [f"--test-arg-{i}"])
    default: str = Sequence(lambda i: f"value_{i}")
    help_message: str = Sequence(lambda i: f"Test help message number {i}")


def test_provided_arguments_have_appropriate_values() -> None:
    input_args = [FullArgumentDataFactory(names=[f"--arg-{i}"]) for i in range(3)]
    cli_args = ["--arg-0", "value_0", "--arg-1", "value_1", "--arg-2", "value_2"]

    with patch_cli_args(cli_args):
        actual_args = get_cmd_line_args(input_args)

    for i in range(3):
        assert actual_args.__getattribute__(f"arg_{i}") == f"value_{i}"


def test_not_provided_required_arguments_display_appropriate_message(capsys: CaptureFixture) -> None:
    input_args = [FullArgumentDataFactory(default=...) for _ in range(3)]

    with patch_cli_args([]), pytest.raises(SystemExit):
        get_cmd_line_args(input_args)

    output = capsys.readouterr().err
    assert "the following arguments are required" in output

    for arg_data in input_args:
        names = "/".join(arg_data.names)
        assert names in output


def test_not_provided_not_required_arguments_fallback_to_defaults() -> None:
    input_args = [FullArgumentDataFactory() for _ in range(3)]

    with patch_cli_args([]):
        args = get_cmd_line_args(input_args)

    for arg in input_args:
        assert get_arg_value_from_namespace(arg.names, args) == arg.default


def test_arguments_abbreviations_are_not_allowed(capsys: CaptureFixture) -> None:
    input_args = [FullArgumentDataFactory(names=[f"--{name}_arg"]) for name in ("first", "second", "third")]
    cli_args = ["--first", "value", "--second", "value", "--third", "value"]

    with patch_cli_args(cli_args), pytest.raises(SystemExit):
        get_cmd_line_args(input_args)

    capsys.readouterr()
