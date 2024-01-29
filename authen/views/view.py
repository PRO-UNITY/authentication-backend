from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.filters import SearchFilter
from authen.models import Country, Gender
from utils.renderers import UserRenderers
from rest_framework.permissions import IsAuthenticated
from authen.models import CustomUser
from authen.serializers.auth_serliazers import UserInformationSerializer
from utils.pagination import StandardResultsSetPagination, Pagination
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
    
class UsersViws(APIView, Pagination):
    render_classes = [UserRenderers]
    permission = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination
    serializer_class = UserInformationSerializer

    def get(self, request):
        queryset = CustomUser.objects.all().order_by('-id')
        page = super().paginate_queryset(queryset)
        if page is not None:
            serializer = super().get_paginated_response(self.serializer_class(page, many=True, context={"request": request}).data)
        else:
            serializer = self.serializer_class(queryset, many=True)
        return success_response(serializer.data)