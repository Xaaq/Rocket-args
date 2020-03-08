import sys
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, TypeVar

from rocket_args.utils import Field


def cast_args_to_fields_types(args: Mapping[str, Optional[str]], fields_data: Sequence[Field]) -> Dict[str, Any]:
    field_name_to_type = {field.name: field.type for field in fields_data}
    name_to_type_to_value = [(name, value, field_name_to_type.get(name, None)) for name, value in args.items()]
    name_to_value = {name: __cast_value_to_type(value, type_hint) for name, value, type_hint in name_to_type_to_value}
    return name_to_value


T = TypeVar("T", bound=Any)


def __cast_value_to_type(value: Optional[str], type_hint: T) -> Optional[T]:
    if value is None or type_hint is None:
        return value
    elif type(type_hint) in [type(List), type(Set)]:
        raw_type = __type_hint_to_raw_type(type_hint)
        subtype = type_hint.__args__[0]
        parsed_value = [subtype(arg) for arg in value.split(",")]
        return raw_type(parsed_value)
    else:
        return type_hint(value)


def __type_hint_to_raw_type(type_hint: Any) -> Any:
    if sys.version_info.minor >= 7:
        raw_type = type_hint.__origin__
    else:
        raw_type = list if issubclass(type_hint, list) else set if issubclass(type_hint, set) else None

        if raw_type is None:
            raise ValueError(f"Unsupported type: {type_hint}")

    return raw_type
