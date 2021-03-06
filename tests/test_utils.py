from typing import List, Tuple

import pytest

from rocket_args import Argument
from rocket_args.utils import Field, MessageBuilder
from tests.utils import FieldFactory


class TestField:
    class TestCliNames:
        @staticmethod
        def test_returns_custom_names() -> None:
            expected_cli_names = ["-a", "--arg"]
            field_data = FieldFactory(value=Argument(cli_names=expected_cli_names))

            assert field_data.cli_names == expected_cli_names

        @staticmethod
        def test_generates_name_based_on_field() -> None:
            field_data = FieldFactory(name="field_name", value=Argument(cli_names=True))
            assert field_data.cli_names == ["--field-name"]

        @staticmethod
        def test_returns_none_if_cli_names_are_turned_off() -> None:
            field_data = FieldFactory(value=Argument(cli_names=False))
            assert field_data.cli_names is None

    class TestEnvName:
        @staticmethod
        def test_returns_custom_name() -> None:
            expected_name = "ARG"
            field_data = FieldFactory(value=Argument(env_name=expected_name))

            assert field_data.env_name == expected_name

        @staticmethod
        def test_generates_name_based_on_field() -> None:
            field_data = FieldFactory(name="field_name", value=Argument(env_name=True))
            assert field_data.env_name == "FIELD_NAME"

        @staticmethod
        def test_returns_none_if_env_name_is_turned_off() -> None:
            field_data = FieldFactory(value=Argument(env_name=False))
            assert field_data.env_name is None


FieldsWithTokens = Tuple[List[Field], List[List[str]]]


class TestMessageBuilder:
    @staticmethod
    @pytest.fixture
    def fields_with_expected_tokens() -> FieldsWithTokens:
        fields = [
            FieldFactory(name="name_1", value=Argument(cli_names=True, env_name=False, help="help 1")),
            FieldFactory(name="name_2", value=Argument(cli_names=False, env_name=True, help="help 2")),
            FieldFactory(name="name_3", value=Argument(cli_names=True, env_name=True, help="help 3")),
            FieldFactory(name="name_4", value=Argument(cli_names=["-a", "--arg"], env_name="ARG", help="help 4")),
        ]
        expected_tokens = [
            ["--name-1", "help 1"],
            ["NAME_2", "help 2"],
            ["--name-3", "NAME_3", "help 3"],
            ["-a", "--arg", "ARG", "help 4"],
        ]
        return fields, expected_tokens

    @staticmethod
    def test_create_help_message(fields_with_expected_tokens: FieldsWithTokens) -> None:
        fields, expected_tokens = fields_with_expected_tokens
        builder = MessageBuilder(fields)

        help_message = builder.create_help_message()
        divided_message = help_message.split("\n")

        for tokens in expected_tokens:
            matches = [all([token in line for token in tokens]) for line in divided_message]
            assert any(matches)

    @staticmethod
    def test_create_missing_arguments_message(fields_with_expected_tokens: FieldsWithTokens) -> None:
        fields, expected_tokens = fields_with_expected_tokens

        builder = MessageBuilder(fields)

        help_message = builder.create_missing_arguments_message()
        divided_message = help_message.split("\n")

        for tokens in expected_tokens:
            matches = [all([token in line for token in tokens]) for line in divided_message]
            assert any(matches)
