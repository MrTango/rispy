"""Miscellaneous functions."""

from copy import deepcopy

from .config import TYPE_OF_REFERENCE_MAPPING


def invert_dictionary(mapping: dict) -> dict:
    """Invert the keys and values of a dictionary."""
    remap = {v: k for k, v in mapping.items()}
    if len(remap) != len(mapping):
        raise ValueError("Dictionary cannot be inverted; some values were not unique")
    return remap


def convert_reference_types(
    reference_list: list[dict],
    reverse: bool = False,
    strict: bool = False,
    type_map: dict = TYPE_OF_REFERENCE_MAPPING,
) -> list:
    """Convert RIS reference types to pretty names.

    This method takes a list of references and returns a copy with converted
    reference types.

    Args:
        reference_list (List[Dict]): A list of references.
        reverse (bool, optional): Convert in reverse.
        strict (bool, optional): Raise error if type not found.
        type_map (Dict, optional): Dict used to map types. Default is
                                   TYPE_OF_REFERENCE_MAPPING.

    Returns:
        list: Returns list of RIS entries.

    """

    def convert(ref, d=type_map):
        old_type = ref["type_of_reference"]
        try:
            ref["type_of_reference"] = d[old_type]
        except KeyError as err:
            if strict and old_type not in d.values():
                raise KeyError(f'Type "{old_type}" not found.') from err
        return ref

    if not reverse:
        return [convert(r) for r in deepcopy(reference_list)]
    else:
        return [convert(r, invert_dictionary(type_map)) for r in deepcopy(reference_list)]
