from rocket_args.utils import var_name_to_arg_name


def test_var_name_to_arg_name():
    input_arg = "arg_name_012"
    expected_arg = "--arg-name-012"

    actual_value = var_name_to_arg_name(input_arg)
    assert actual_value == expected_arg
