from rocket_args import Argument
from rocket_args.utils import Field


class TestField:
    class TestCliNames:
        @staticmethod
        def test_returns_custom_names() -> None:
            expected_cli_names = ["-a", "--arg"]
            field_data = Field(name="field_name", type=str, value=Argument(cli_names=expected_cli_names))

            actual_cli_names = field_data.cli_names

            assert actual_cli_names == expected_cli_names

        @staticmethod
        def test_generates_name_based_on_field_name() -> None:
            field_data = Field(name="field_name", type=str, value=Argument(cli_names=True))
            cli_names = field_data.cli_names
            assert cli_names == ["--field-name"]

        @staticmethod
        def test_returns_none_if_cli_names_are_turned_off() -> None:
            field_data = Field(name="field_name", type=str, value=Argument(cli_names=False))
            assert field_data.cli_names is None

    class TestEnvName:
        @staticmethod
        def test_returns_custom_name() -> None:
            expected_name = "ARG"
            field_data = Field(name="field_name", type=str, value=Argument(env_name=expected_name))

            actual_name = field_data.env_name

            assert actual_name == expected_name

        @staticmethod
        def test_generates_name_based_on_field_name() -> None:
            field_data = Field(name="field_name", type=str, value=Argument(env_name=True))
            env_name = field_data.env_name
            assert env_name == "FIELD_NAME"

        @staticmethod
        def test_returns_none_if_env_name_is_turned_off() -> None:
            field_data = Field(name="field_name", type=str, value=Argument(env_name=False))
            assert field_data.env_name is None
