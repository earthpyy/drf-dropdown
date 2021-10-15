import typing
from importlib import import_module

from django.apps import apps

from dropdown import serializers, types
from dropdown.registry import default_registry


class DropdownGetter:
    """Getting dropdown from dropdown.py in each applications"""

    def __init__(self, types_: typing.List[str], *, query: str = None, **kwargs):
        self.types = types_
        self.query = query or ''
        self.kwargs = kwargs

        self._load_all_dropdown_data()

    def _load_all_dropdown_data(self):
        for app in apps.app_configs.values():
            try:
                import_module(f'{app.name}.dropdown')
            except ImportError:
                continue

        self.data = default_registry.registry

    def _get_dropdown_from_type(self, type_: str) -> typing.Tuple[typing.List[types.DropdownItem], int]:
        """
        Get dropdown from dropdown data

        @return: list of dropdown items and total amount of items
        """
        data = self.data.get(type_)
        if not data:
            raise ValueError(f'No data found for type \'{type_}\'.')

        if not callable(data):
            raise ValueError('Data is invalid.')

        res = data(query=self.query, **self.kwargs)

        if isinstance(res, tuple):
            return res
        return res, len(res)

    @staticmethod
    def _serialize_items(items: typing.List[types.DropdownItem]) -> typing.List[typing.Dict[str, typing.Any]]:
        return serializers.DropdownItemSerializer(items, many=True).data

    def get(
        self,
        serialized=False
    ) -> typing.Dict[str, typing.Union[typing.List[typing.Union[types.DropdownItem, typing.Dict[str, typing.Any]]], typing.Dict[str, int]]]:
        result = {}
        count = {}

        for type_ in self.types:
            result[type_], count[type_] = self._get_dropdown_from_type(type_)

            if serialized:
                result[type_] = self._serialize_items(result.pop(type_))
                count[type_] = count.pop(type_)

        # add count
        result['_count'] = count

        return result
