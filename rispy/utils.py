"""Miscellaneous functions."""

from typing import Dict, List
from copy import deepcopy

from .config import TYPE_OF_REFERENCE_MAPPING


def invert_dictionary(mapping: Dict) -> Dict:
    """Invert the keys and values of a dictionary."""
    remap = {v: k for k, v in mapping.items()}
    if len(remap) != len(mapping):
        raise ValueError("Dictionary cannot be inverted; some values were not unique")
    return remap


def pretty_reference_types(
    reference_list: List,
    reverse: bool = False,
    strict: bool = False,
    type_map: Dict = TYPE_OF_REFERENCE_MAPPING,
) -> List:
    """Convert RIS reference types to pretty names."""

    def convert(ref, d=type_map):
        old_type = ref["type_of_reference"]
        try:
            ref["type_of_reference"] = d[old_type]
        except KeyError:
            if strict and old_type not in d.values():
                raise KeyError(f'Type "{old_type}" not found.')
        return ref

    if not reverse:
        return [convert(r) for r in deepcopy(reference_list)]
    else:
        return [convert(r, invert_dictionary(type_map)) for r in deepcopy(reference_list)]
