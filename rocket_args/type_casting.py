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
    type_of_field_type = type(target_type)

    if type_of_field_type in [type(List), type(Tuple), type(Set)]:
        real_type = __type_hint_to_callable_type(target_type)
        subtype = target_type.__args__[0]
        divided_arg = [subtype(arg) for arg in value.split(",")]
        return real_type(divided_arg)
    else:
        return target_type(value)


def __type_hint_to_callable_type(type_hint: Any) -> Any:
    return (
        list
        if issubclass(type_hint, list)
        else tuple
        if issubclass(type_hint, tuple)
        else set
        if issubclass(type_hint, set)
        else type_hint.__origin__
    )
