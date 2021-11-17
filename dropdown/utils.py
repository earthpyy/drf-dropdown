import collections
import operator
import typing


def dot_to_relation(value: str) -> str:
    return value.replace('.', '__')


def remove_duplication(value: typing.Iterable) -> list:
    return list(collections.OrderedDict.fromkeys(value))


def attrgetter(obj: dict, key: str, raise_exception=True, default=None):
    try:
        return operator.attrgetter(key)(obj)
    except AttributeError:
        if raise_exception:
            raise

    return default
