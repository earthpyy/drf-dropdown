import typing


class DropdownRequest(typing.TypedDict):
    types: typing.List[str]
    query: typing.Optional[str]
    kwargs: typing.Dict[str, typing.Any]


class DropdownItem:

    def __init__(self, value: typing.Optional[typing.Any], label: str = None, context: dict = None):
        self.value = value
        self.label = label or str(value or '')
        self.context = context or {}
