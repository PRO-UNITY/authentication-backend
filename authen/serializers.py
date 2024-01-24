from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth.models import Group
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.core.validators import MaxLengthValidator
from authen.models import CustomUser, Country, Gender
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed


class CountrySerilaizers(serializers.ModelSerializer):
    
    class Meta:
        model = Country
        fields = '__all__'


class GenderSerializers(serializers.ModelSerializer):

    class Meta:
        model = Gender
        fields = '__all__'


class UserSignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, validators=[
            MaxLengthValidator(limit_value=50, message="First name cannot exceed 50 characters.")],)
    last_name = serializers.CharField(max_length=50, validators=[
            MaxLengthValidator(limit_value=50, message="Last name cannot exceed 50 characters."),])
    username = serializers.CharField(max_length=255, required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "email", "country", "phone", "gender", "password", "confirm_password",]
        extra_kwargs = {"first_name": {"required": True}, "last_name": {"required": True}}

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password', None)

        if validated_data["password"] != confirm_password:
            raise serializers.ValidationError({"error": "Those passwords don't match"})
        create = get_user_model().objects.create_user(**validated_data)
        return create


class UserUpdateSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, validators=[
            MaxLengthValidator(limit_value=50, message="First name cannot exceed 50 characters."),],)
    last_name = serializers.CharField(max_length=50, validators=[
            MaxLengthValidator(limit_value=50, message="Last name cannot exceed 50 characters."),],)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=CustomUser.objects.all())])

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "email", "country", "phone", "gender"]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.email = validated_data.get("email", instance.email)
        instance.country = validated_data['country', instance.country]
        instance.gender = validated_data["gender", instance.gender]
        instance.save()
        return instance


class UserSigInSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, min_length=2)
    password = serializers.CharField(max_length=50, min_length=1)

    class Meta:
        model = CustomUser
        fields = ["username", "password"]
        read_only_fields = ("username",)

    def validate(self, data):
        if self.context.get("request") and self.context["request"].method == "POST":
            allowed_keys = set(self.fields.keys())
            input_keys = set(data.keys())
            extra_keys = input_keys - allowed_keys
            if extra_keys:
                raise serializers.ValidationError(f"Additional keys are not allowed: {', '.join(extra_keys)}")
        return data


class UserInformationSerializer(serializers.ModelSerializer):
    country = CountrySerilaizers(read_only=True)
    gender = GenderSerializers(read_only=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "email", "country", "phone", "gender"]



class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    default_error_message = {"bad_token": ("Token is expired or invalid")}

    def validate(self, attrs):
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail("bad_token")


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