from rest_framework import serializers
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed



class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ["email",]


class PasswordResetCompleteSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=8, max_length=32, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ["password", "token", "uidb64"]

    def validate(self, attrs):
        try:
            password = attrs.get("password")
            token = attrs.get("token")
            uidb64 = attrs.get("uidb64")

            user_id = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(id=user_id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed("Invalid link", 401)

            user.set_password(password)
            user.save()
            return user
        except Exception:
            raise AuthenticationFailed("Invalid link", 401)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)