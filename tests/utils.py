import argparse
import os
from contextlib import contextmanager
from typing import Generator, List


@contextmanager
def patch_cli_args(fake_cli_args: List[str]) -> Generator[None, None, None]:
    defaults = argparse.ArgumentParser.parse_args.__defaults__
    argparse.ArgumentParser.parse_args.__defaults__ = (fake_cli_args, None)
    yield
    argparse.ArgumentParser.parse_args.__defaults__ = defaults


@contextmanager
def patch_env(**name_to_var: str) -> Generator[None, None, None]:
    for name, value in name_to_var.items():
        os.environ[name] = value

    yield

    for name in name_to_var.keys():
        del os.environ[name]
