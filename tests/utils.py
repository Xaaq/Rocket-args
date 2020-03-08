import os
from contextlib import contextmanager
from typing import Any, Generator, List
from unittest.mock import patch

from factory import Factory, Sequence

from rocket_args import Argument
from rocket_args.utils import Field


@contextmanager
def patch_cli_args(fake_cli_args: List[str]) -> Generator[None, None, None]:
    with patch("sys.argv", ["program_name"] + fake_cli_args):
        yield


@contextmanager
def patch_env_args(**name_to_var: str) -> Generator[None, None, None]:
    for name, value in name_to_var.items():
        os.environ[name] = value

    yield

    for name in name_to_var.keys():
        del os.environ[name]


class FieldFactory(Factory):
    class Meta:
        model = Field

    name: str = Sequence(lambda i: f"name_{i}")
    type: Any = str
    value: Argument = Argument()
