from rocket_args.main import RocketBase
from tests.test_get_cmd_line_args import patch_cli_args


def test_provided_arguments_return_appropriate_values():
    class Args(RocketBase):
        arg_int: int
        arg_str: str
        arg_float: float

    input_args = ["--arg-int", "123", "--arg-str", "abc", "--arg-float", "123.456"]

    with patch_cli_args(input_args):
        output_args = Args.parse_args()

    assert output_args.arg_int == 123
    assert output_args.arg_str == "abc"
    assert output_args.arg_float == 123.456


def test_not_provided_arguments_fallback_to_defaults():
    class Args(RocketBase):
        arg_int: int = 123
        arg_str: str = "abc"
        arg_float: float = 123.456

    with patch_cli_args([]):
        output_args = Args.parse_args()

    assert output_args.arg_int == 123
    assert output_args.arg_str == "abc"
    assert output_args.arg_float == 123.456