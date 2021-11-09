import collections
import typing


def dot_to_relation(value: str) -> str:
    return value.replace('.', '__')


def remove_duplication(value: typing.Iterable) -> list:
    return list(collections.OrderedDict.fromkeys(value))
