import typing

from django.conf import settings
from django.core import exceptions
from django.db import models

from dropdown import types

try:
    DROPDOWN_LIMIT = settings.DROPDOWN['LIMIT']
except (exceptions.ImproperlyConfigured, AttributeError, IndexError):
    DROPDOWN_LIMIT = 100


def from_model(
    model,
    label_field: str = None,
    value_field='pk',
    q_filter: models.Q = None,
    no_limit=True,
    context_fields: typing.List[str] = None,
) -> typing.Tuple[typing.List[types.DropdownItem], int]:
    """
    Get dropdown items from given model

    @param model: model to get dropdown
    @param label_field: name of field which will be label (default is `__str__`)
    @param value_field: name of field which will be value (default is `pk`)
    @param q_filter: additional filter
    @param no_limit: no items limit (overriding `LIMIT` in settings)
    @param context_fields: additional fields to be appear in context in each dropdown item
    @return: tuple of dropdown items and item count
    """

    # initial queryset
    queryset = model.objects.all()

    # filter
    if q_filter:
        queryset = queryset.filter(q_filter)

    # values
    values = {value_field}
    if label_field:
        values.add(label_field)
    for context_field in (context_fields or []):
        values.add(context_field)
    queryset = queryset.values(*values)

    # order
    queryset = queryset.order_by(label_field or value_field)

    # distinct
    queryset = queryset.distinct()

    # limit & count
    if not no_limit and DROPDOWN_LIMIT:
        count = queryset.count()
        result_list = list(queryset[:DROPDOWN_LIMIT])
    else:
        result_list = list(queryset)
        count = len(result_list)

    # results
    return [
        types.DropdownItem(
            label=x[label_field] if label_field is not None else str(x),
            value=x[value_field],
            context={y: x[y] for y in (context_fields or [])},
        ) for x in result_list
    ], count


def from_choices(choices: models.Choices) -> typing.Tuple[typing.List[types.DropdownItem], int]:
    """
    Get dropdown items from given model choices

    @param choices: choices to get dropdown
    """

    return [types.DropdownItem(label=x.label, value=x.value) for x in sorted(choices, key=lambda x: x.label)]
