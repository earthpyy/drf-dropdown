import typing


class DropdownItem:
    """Dropdown item to be populated"""

    def __init__(self, value: typing.Optional[typing.Any], label: str = None, context: dict = None):
        self.value = value
        self.label = label or str(value or '')
        self.context = context or {}
