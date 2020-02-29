from argparse import Namespace
from typing import Sequence
from unittest.mock import call, patch

import pytest

from rocket_args.cli_utils import FullArgumentData, get_arg_from_namespace, get_cmd_line_args, var_name_to_arg_name


def test_var_name_to_arg_name() -> None:
    input_arg = "arg_name_012"
    expected_arg = "--arg-name-012"

    actual_value = var_name_to_arg_name(input_arg)
    assert actual_value == expected_arg


def test_get_cmd_line_args() -> None:
    args = [
        FullArgumentData(names=["-a1", "--arg-1"], default=..., is_required=True, help="help message 1"),
        FullArgumentData(names=["-a2", "--arg-2"], default="default", is_required=False, help="help message 2"),
    ]

    with patch("argparse.ArgumentParser.parse_args"), patch("argparse.ArgumentParser.add_argument") as add_argument:
        get_cmd_line_args(args)

    calls = [call(*arg.names, default=arg.default, required=arg.is_required, help=arg.help) for arg in args]
    add_argument.assert_has_calls(calls)


@pytest.mark.parametrize(
    "cli_arg_names, namespace",
    [
        [["-a"], Namespace(a="value")],
        [["-a-"], Namespace(a_="value")],
        [["-arg"], Namespace(arg="value")],
        [["-arg-"], Namespace(arg_="value")],
        [["--arg"], Namespace(arg="value")],
        [["--arg-"], Namespace(arg_="value")],
        [["-arg-with-dashes"], Namespace(arg_with_dashes="value")],
        [["--arg-with-dashes"], Namespace(arg_with_dashes="value")],
        [["----arg-with-dashes"], Namespace(arg_with_dashes="value")],
        [["-a", "--arg"], Namespace(arg="value")],
        [["-a", "----arg"], Namespace(arg="value")],
        [["-a", "--arg-1", "--arg-2"], Namespace(arg_1="value")],
        [["-a", "--arg-1", "----arg-2"], Namespace(arg_1="value")],
        [["-a", "----arg-1", "--arg-2"], Namespace(arg_1="value")],
    ],
    ids=[
        "1-dash short arg name",
        "1-dash short arg name with end dash",
        "1-dash long arg name",
        "1-dash long arg name with end dash",
        "2-dash arg name",
        "2-dash arg name with end dash",
        "1-dash arg with dashes",
        "2-dash arg with dashes",
        "4-dash arg with dashes",
        "1 and 2-dash args",
        "1 and 4-dash args",
        "1, 2 and 2-dash args",
        "1, 2 and 4-dash args",
        "1, 4 and 2-dash args",
    ],
)
def test_get_arg_from_namespace(cli_arg_names: Sequence[str], namespace: Namespace) -> None:
    result = get_arg_from_namespace(namespace, cli_arg_names)
    assert result == "value"
