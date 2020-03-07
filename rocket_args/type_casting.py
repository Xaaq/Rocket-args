import sys
from typing import Any, Dict, List, Mapping, Optional, Sequence, Set, Tuple, TypeVar

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
    raw_type, subtypes = __get_raw_type_data(target_type)
    parsed_value = [subtypes[0](arg) for arg in value.split(",")] if raw_type in [list, set] else value
    return raw_type(parsed_value)


def __get_raw_type_data(type_hint: Any) -> Tuple[Any, List[Any]]:
    if type(type_hint) in [type(List), type(Set)]:
        if sys.version_info.minor >= 7:
            raw_type = type_hint.__origin__
        else:
            if issubclass(type_hint, list):
                raw_type = list
            elif issubclass(type_hint, set):
                raw_type = set
            else:
                raise ValueError(f"Unsupported type: {type_hint}")

        return raw_type, type_hint.__args__
    else:
        return type_hint, []
