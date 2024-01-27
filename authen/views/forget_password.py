from django.utils.http import urlsafe_base64_encode
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework import generics
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from authen.models import CustomUser
from utils.forget_password_utils import Util
from django.utils.encoding import smart_bytes
from utils.responses import (
    user_not_found_response,
    success_response,
    bad_request_response
)
from authen.serializers.forget_pass_serializers import (
    ResetPasswordSerializer,
    PasswordResetCompleteSerializer,
    ChangePasswordSerializer
    
)


class RequestPasswordRestEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema(request_body=ResetPasswordSerializer)
    @action(methods=['post'], detail=False)
    def post(self, request):
        email = request.data.get("email")
        if CustomUser.objects.filter(email=email).exists():
            user = CustomUser.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            absurl = f"http://localhost:3000/reset-password/{uidb64}/{token}"

            email_body = f"Hi \n Use link below to reset password \n link: {absurl}"
            data = {"email_body": email_body, "to_email": user.email, "email_subject": "Reset your password",}
            Util.send(data)
            return success_response("send email")
        return user_not_found_response("This email is not found..")


class SetNewPasswordView(generics.GenericAPIView):
    serializer_class = PasswordResetCompleteSerializer

    @action(methods=['patch'], detail=False)
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return success_response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def change_password(request):
    if request.method == "POST":
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            if user.check_password(serializer.data.get("old_password")):
                user.set_password(serializer.data.get("new_password"))
                user.save()
                update_session_auth_hash(request, user)
                return success_response("Password changed successfully.")
            return bad_request_response("Incorrect old password.")
        return bad_request_response(serializer.errors)
