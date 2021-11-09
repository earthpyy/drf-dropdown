import typing


class DropdownItem:
    """Dropdown item to be populated"""

    def __init__(self, value: typing.Optional[typing.Any], label: str = None, context: dict = None):
        self.value = value
        self.label = label or str(value or '')
        self.context = context or {}

    def __eq__(self, o: object) -> bool:
        return self.value == o.value and self.label == o.label and self.context == self.context

    def __hash__(self) -> int:
        return hash((self.value, self.label, self.context))
