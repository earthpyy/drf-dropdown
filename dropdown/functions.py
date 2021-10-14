from dropdown import getter, serializers


def get_dropdown_from_request(request):
    # validate params
    serializer = serializers.DropdownRequestSerializer(data=request.query_params, context={'request': request})
    serializer.is_valid(raise_exception=True)
    request_data = serializer.save()

    # getting data
    getter_class = getter.DropdownGetter(
        request_data['types'],
        query=request_data.get('query'),
        request=request,
        **request_data['kwargs'],
    )
    result = getter_class.get(serialized=True)
    return result
