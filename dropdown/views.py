from operator import itemgetter

from rest_framework.response import Response
from rest_framework.views import APIView

from dropdown import functions


class DropdownView(APIView):
    """View for getting dropdown list from types"""

    def get(self, request):
        result = functions.get_dropdown_from_request(request)

        for item in result:
            if item == '_count':
                continue
            result[item] = sorted(result[item], key=itemgetter('label'))

        return Response(result)
