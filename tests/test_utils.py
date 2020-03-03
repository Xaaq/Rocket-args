from rocket_args import Argument
from rocket_args.utils import Field


class TestFieldCliNames:
    @staticmethod
    def test_take_custom_names() -> None:
        expected_cli_names = ["-a", "--arg"]
        field_data = Field(name="field_name", type=str, value=Argument(cli_names=expected_cli_names))

        actual_cli_names = field_data.cli_names

        assert actual_cli_names == expected_cli_names

    @staticmethod
    def test_generate_name_based_on_field_name() -> None:
        field_data = Field(name="field_name", type=str, value=Argument())
        cli_names = field_data.cli_names
        assert cli_names == ["--field-name"]
