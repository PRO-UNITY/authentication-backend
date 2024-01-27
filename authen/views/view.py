from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from authen.models import Country, Gender
from utils.responses import (
    user_not_found_response,
    success_response
)
from authen.serializers.serializer import (
    CountrySerilaizers,
    GenderSerializers
)


class CountrViews(APIView):
    filter_backends = [SearchFilter]
    search_fields = ['name'] 

    def get(self, request):
        queryset = Country.objects.all()
        name = request.query_params.get("name", None)
        if name:
            queryset = queryset.filter(Q(name__icontains=name))
            if not queryset.exists():
                return user_not_found_response('Node found')
        serializer = CountrySerilaizers(queryset, many=True)
        return success_response(serializer.data)


class GenderViews(APIView):
    filter_backends = [SearchFilter]
    search_fields = ['name'] 

    def get(self, request):
        objects_list = Gender.objects.all()
        serializers = GenderSerializers(objects_list, many=True)
        return success_response(serializers.data)