import typing


def dot_to_relation(value: str) -> str:
    return value.replace('.', '__')


def extract_select_related(value: str) -> typing.Optional[str]:
    split_value = value.split('.')

    return '__'.join(split_value[:-1]) or None
