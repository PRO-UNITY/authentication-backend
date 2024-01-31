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