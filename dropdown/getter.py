import typing

from django.apps import apps
from django.utils.module_loading import import_string

from dropdown import serializers, types


class DropdownGetter:
    """Getting dropdown from dropdown.py in each applications"""

    def __init__(self, types_: typing.List[str], *, query: str = None, **kwargs):
        self.types = types_
        self.query = query or ''
        self.kwargs = kwargs

        self.data = self._load_all_dropdown_data()

    @staticmethod
    def _load_all_dropdown_data() -> typing.Dict[str, typing.Callable]:
        dropdown_data = {}
        for app in apps.app_configs.values():
            try:
                data = import_string(f'{app.name}.dropdown.DROPDOWN')
            except ImportError:
                continue

            if not isinstance(data, dict):
                raise ValueError('DROPDOWN is not `dict` instance.')

            dropdown_data.update(data)

        return dropdown_data

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
