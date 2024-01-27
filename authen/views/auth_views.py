from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from utils.renderers import UserRenderers
from authen.models import CustomUser
from utils.expected_fields import check_required_key
from utils.permissions import login_permissions
from utils.responses import (
    bad_request_response,
    success_created_response,
    user_not_found_response,
    success_response
)
from authen.serializers.auth_serliazers import (
    UserSignUpSerializer,
    UserSigInSerializer,
    UserUpdateSerializer,
    UserInformationSerializer,
)


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}


class UserSignUp(APIView):
    render_classes = [UserRenderers]

    @action(methods=['post'], detail=False)
    @swagger_auto_schema(request_body=UserSignUpSerializer, responses={201: "Created - Item created successfully",}, tags=["auth"],)
    def post(self, request):
        if self.validate_fields(request):
            return bad_request_response(f"Unexpected fields: {', '.join(self.validate_fields(request))}")

        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            instanse = serializer.save()
            token = get_token_for_user(instanse)
            return success_created_response(token)
        return bad_request_response(serializer.errors)
    
    def validate_fields(self, request):
        valid_fields = {"username", "email", "country", "phone", "gender", "password", "confirm_password"}
        return check_required_key(request, valid_fields)


class UserSignIn(APIView):
    render_classes = [UserRenderers]

    @action(methods=['post'], detail=True)
    @swagger_auto_schema(request_body=UserSigInSerializer, responses={201: "Created - Item created successfully",}, tags=["auth"],)
    def post(self, request):
        if self.validate_fields(request):
            return bad_request_response(f"Unexpected fields: {', '.join(self.validate_fields(request))}")
        serializer = self.validate_serializer(request)
        if serializer.is_valid(raise_exception=True):
            return self.authenticate_user(request)
        return bad_request_response(serializer.errors)

    def validate_fields(self, request):
        valid_fields = {"id", "username", "password"}
        return check_required_key(request, valid_fields)

    def validate_serializer(self, request):
        serializer = UserSigInSerializer(data=request.data, partial=True)
        return serializer

    def authenticate_user(self, request):
        username = request.data["username"]
        password = request.data["password"]
        user = authenticate(username=username, password=password)
        if user is not None:
            tokens = get_token_for_user(user)
            return success_response(tokens)
        else:
            return user_not_found_response("user not found")


class UserProfile(APIView):
    render_classes = [UserRenderers]
    permission = [IsAuthenticated]

    @login_permissions
    def get(self, request, *args, **kwarg):
        serializer = UserInformationSerializer(request.user, context={"request": request})
        return success_response(serializer.data)

    @login_permissions
    @action(methods=['put'], detail=True)
    @swagger_auto_schema(request_body=UserUpdateSerializer, responses={201: "update - Item update successfully",}, tags=["auth"],)
    def put(self, request, *args, **kwarg):
        if self.validate_fields(request):
            return bad_request_response(f"Unexpected fields: {', '.join(self.validate_fields(request))}")
        queryset = CustomUser.objects.filter(id=request.user.id)[0]
        serializer = UserUpdateSerializer(context={"request": request}, instance=queryset, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return success_response(serializer.data)

    def validate_fields(self, request):
        valid_fields = {"id", "username", "first_name", "last_name", "email", "country", "phone", "gender"}
        return check_required_key(request, valid_fields)

    @login_permissions
    def delete(self, request):
        user_delete = CustomUser.objects.get(id=request.user.id)
        user_delete.delete()
        return success_response("user delete")
