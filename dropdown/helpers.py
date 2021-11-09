import operator
import typing

from django.conf import settings
from django.core import exceptions
from django.db import models

from dropdown import types, utils

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
    select_related: typing.List[str] = None,
) -> typing.Tuple[typing.List[types.DropdownItem], int]:
    """
    Get dropdown items from given model

    @param model: model to get dropdown
    @param label_field: name of field which will be label (default is `__str__`)
    @param value_field: name of field which will be value (default is `pk`)
    @param q_filter: additional filter
    @param no_limit: no items limit (overriding `LIMIT` in settings)
    @param context_fields: additional fields to be appear in context in each dropdown item
    @param select_related: fields to select related
    @return: tuple of dropdown items and item count
    """
    if context_fields is None:
        context_fields = []

    # initial queryset
    queryset = model.objects.all()

    # select related
    # NOTE: prefetch related is not supported
    if select_related is not None:
        queryset = queryset.select_related(*select_related)

    # filter
    if q_filter:
        queryset = queryset.filter(q_filter)

    # only
    if label_field is not None:
        only_fields = [
            utils.dot_to_relation(label_field),
            utils.dot_to_relation(value_field),
            *[utils.dot_to_relation(x) for x in context_fields],
        ]
        queryset = queryset.only(*only_fields)

    # order
    order_by = label_field or value_field
    queryset = queryset.order_by(utils.dot_to_relation(order_by))

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
    return utils.remove_duplication(
        types.DropdownItem(
            label=operator.attrgetter(label_field)(x) if label_field is not None else str(x),
            value=operator.attrgetter(value_field)(x),
            context={y: operator.attrgetter(y)(x) for y in (context_fields)},
        ) for x in result_list
    ), count


def from_choices(choices: models.Choices) -> typing.Tuple[typing.List[types.DropdownItem], int]:
    """
    Get dropdown items from given model choices

    @param choices: choices to get dropdown
    """

    return utils.remove_duplication(types.DropdownItem(label=x.label, value=x.value) for x in sorted(choices, key=lambda x: x.label))
