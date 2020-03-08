import sys
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, TypeVar

from rocket_args.utils import Field


def cast_args_to_fields_types(args: Mapping[str, Optional[str]], fields_data: Sequence[Field]) -> Dict[str, Any]:
    field_name_to_type = {field.name: field.type for field in fields_data}
    name_to_type_to_value = [(name, field_name_to_type.get(name, None), value) for name, value in args.items()]
    name_to_value = {
        name: value if (type_hint is None or value is None) else __cast_value_to_type(value, type_hint)
        for name, type_hint, value in name_to_type_to_value
    }
    return name_to_value


T = TypeVar("T", bound=Any)


def __cast_value_to_type(value: str, target_type: T) -> T:
    if type(target_type) in [type(List), type(Set)]:
        raw_type = __type_hint_to_raw_type(target_type)
        subtype = target_type.__args__[0]
        parsed_value = [subtype(arg) for arg in value.split(",")]
        return raw_type(parsed_value)
    else:
        return target_type(value)


def __type_hint_to_raw_type(type_hint: Any) -> Any:
    if sys.version_info.minor >= 7:
        raw_type = type_hint.__origin__
    else:
        raw_type = list if issubclass(type_hint, list) else set if issubclass(type_hint, set) else None
        if raw_type is None:
            raise ValueError(f"Unsupported type: {type_hint}")

    return raw_type
