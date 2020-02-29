from argparse import Namespace
from typing import Sequence

import pytest

from rocket_args.cli import get_arg_from_namespace, var_name_to_arg_name


def test_var_name_to_arg_name() -> None:
    input_arg = "arg_name_012"
    expected_arg = "--arg-name-012"

    actual_value = var_name_to_arg_name(input_arg)
    assert actual_value == expected_arg


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
