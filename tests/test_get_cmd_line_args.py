import argparse
import sys
from io import StringIO
from contextlib import contextmanager
from itertools import chain
from typing import Generator, List

import pytest
from factory import Factory, Sequence
from factory.fuzzy import FuzzyChoice

from rocket_args.utils import var_name_to_arg_name, get_cmd_line_args, ArgData


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
    input_args = [ArgDataFactory() for _ in range(10)]
    input_value = "value"

    cli_args = [(var_name_to_arg_name(arg.name), input_value) for arg in input_args]
    cli_args_list = list(chain.from_iterable(cli_args))

    with patch_cli_args(cli_args_list):
        actual_args = get_cmd_line_args(input_args)

    for arg in input_args:
        assert actual_args.__getattribute__(arg.name) == input_value


def test_not_provided_required_arguments_display_appropriate_message() -> None:
    input_args = [ArgDataFactory(is_required=True) for _ in range(10)]

    with patch_cli_args([]), pytest.raises(SystemExit), redirect_stderr() as stderr:
        get_cmd_line_args(input_args)

    output = stderr.getvalue()
    assert "the following arguments are required" in output

    expected_cli_args = [var_name_to_arg_name(arg.name) for arg in input_args]
    for cli_arg_name in expected_cli_args:
        assert cli_arg_name in output


def test_not_provided_not_required_arguments_fallback_to_defaults() -> None:
    input_args = [ArgDataFactory(is_required=False) for _ in range(10)]

    with patch_cli_args([]):
        args = get_cmd_line_args(input_args)

    for arg in input_args:
        assert args.__getattribute__(arg.name) == arg.default


def test_arguments_abbreviations_are_not_allowed() -> None:
    abbreviations = ("first", "second", "third")
    input_args = [ArgDataFactory(name=f"{name}_arg") for name in abbreviations]

    cli_args = [(f"--{name}", "value") for name in abbreviations]
    cli_args_list = list(chain.from_iterable(cli_args))

    with patch_cli_args(cli_args_list), pytest.raises(SystemExit), redirect_stderr():
        get_cmd_line_args(input_args)
