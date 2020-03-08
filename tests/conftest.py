from typing import Any, List, Set, Tuple

import pytest
from _pytest.fixtures import SubRequest


@pytest.fixture(
    params=[
        (str, "abcd", "abcd"),
        (int, "1234", 1234),
        (float, "12.34", 12.34),
        (List[int], "12,34,56,78", [12, 34, 56, 78]),
        (Set[int], "12,34,56,78", {12, 34, 56, 78}),
    ],
    ids=["str", "int", "float", "list of ints", "set of ints"],
)
def type_hint_to_raw_arg_to_parsed_arg(request: SubRequest) -> Tuple[Any, str, Any]:
    return request.param


@pytest.fixture
def type_hint(type_hint_to_raw_arg_to_parsed_arg: Tuple[Any, str, Any]) -> Any:
    return type_hint_to_raw_arg_to_parsed_arg[0]


@pytest.fixture
def raw_arg(type_hint_to_raw_arg_to_parsed_arg: Tuple[Any, str, Any]) -> str:
    return type_hint_to_raw_arg_to_parsed_arg[1]


@pytest.fixture
def parsed_arg(type_hint_to_raw_arg_to_parsed_arg: Tuple[Any, str, Any]) -> Any:
    return type_hint_to_raw_arg_to_parsed_arg[2]
