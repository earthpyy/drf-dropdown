import typing

from rest_framework import serializers as rest_serializers

from dropdown import types


class DropdownRequestSerializer(rest_serializers.Serializer):
    """Serializer for deserialize dropdown request"""

    type = rest_serializers.CharField()
    query = rest_serializers.CharField(required=False, allow_null=True, allow_blank=True)

    def validate_type(self, value: str) -> typing.List[str]:
        return value.split(',')

    def validate(self, attrs):
        # split types
        if attrs.get('query') and len(attrs['type']) > 1:
            raise rest_serializers.ValidationError({'query': 'No query string allowed when using multiple types.'})

        return attrs

    def create(self, validated_data):
        # change key
        validated_data['types'] = validated_data.pop('type')

        # get kwargs
        kwargs = dict(self.initial_data.items())
        kwargs.pop('type')
        kwargs.pop('query', None)

        return {**validated_data, 'kwargs': kwargs}


class DropdownItemSerializer(rest_serializers.Serializer):
    """Serializer for serialize dropdown items"""

    label = rest_serializers.CharField()
    value = rest_serializers.SerializerMethodField(method_name='get_value_')
    context = rest_serializers.SerializerMethodField()

    @staticmethod
    def get_value_(obj: types.DropdownItem):
        return obj.value or ''

    @staticmethod
    def get_context(obj: types.DropdownItem):
        return obj.context or {}
