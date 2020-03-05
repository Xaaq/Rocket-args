import os
from contextlib import contextmanager
from typing import Generator, List
from unittest.mock import patch


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
