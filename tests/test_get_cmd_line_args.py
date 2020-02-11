import argparse
import sys
from contextlib import contextmanager
from io import StringIO
from typing import Generator, List

import pytest
from factory import Factory, Sequence
from factory.fuzzy import FuzzyChoice

from rocket_args.utils import ArgData, get_cmd_line_args, var_name_to_arg_name


class ArgDataFactory(Factory):
    class Meta:
        model = ArgData

    name: str = Sequence(lambda i: f"test_arg_{i}")
    is_required: bool = FuzzyChoice((True, False))
    default: str = Sequence(lambda i: f"value_{i}")


@contextmanager
def patch_cli_args(fake_cli_args: List[str]) -> Generator[None, None, None]:
    defaults = argparse.ArgumentParser.parse_args.__defaults__
    argparse.ArgumentParser.parse_args.__defaults__ = (fake_cli_args, None)
    yield
    argparse.ArgumentParser.parse_args.__defaults__ = defaults


@contextmanager
def redirect_stderr() -> Generator[StringIO, None, None]:
    old_err, new_err = sys.stderr, StringIO()

    sys.stderr = new_err
    yield new_err
    sys.stderr = old_err


def test_provided_arguments_have_appropriate_values() -> None:
    input_args = [ArgDataFactory(name=f"arg_{i}") for i in range(3)]
    cli_args = ["--arg-0", "value_0", "--arg-1", "value_1", "--arg-2", "value_2"]

    with patch_cli_args(cli_args):
        actual_args = get_cmd_line_args(input_args)

    for i in range(3):
        assert actual_args.__getattribute__(f"arg_{i}") == f"value_{i}"


def test_not_provided_required_arguments_display_appropriate_message() -> None:
    input_args = [ArgDataFactory(is_required=True) for _ in range(3)]

    with patch_cli_args([]), pytest.raises(SystemExit), redirect_stderr() as stderr:
        get_cmd_line_args(input_args)

    output = stderr.getvalue()
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


def test_arguments_abbreviations_are_not_allowed() -> None:
    input_args = [ArgDataFactory(name=f"{name}_arg") for name in ("first", "second", "third")]
    cli_args = ["--first", "value", "--second", "value", "--third", "value"]

    with patch_cli_args(cli_args), pytest.raises(SystemExit), redirect_stderr():
        get_cmd_line_args(input_args)
