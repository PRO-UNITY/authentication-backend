from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.core.validators import MaxLengthValidator
from authen.models import CustomUser
from django.contrib.auth import get_user_model


class BaseUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=CustomUser.objects.all())])

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "country", "phone", "gender"]


class UserSignUpSerializer(BaseUserSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ["password", "confirm_password"]

    def create(self, validated_data):
        confirm_password = validated_data.pop('confirm_password', None)

        if validated_data["password"] != confirm_password:
            raise serializers.ValidationError({"error": "Those passwords don't match"})
        create = get_user_model().objects.create_user(**validated_data)
        return create


class UserUpdateSerializer(BaseUserSerializer):
    first_name = serializers.CharField(max_length=50, validators=[MaxLengthValidator(limit_value=50, message="First name cannot exceed 50 characters.")])
    last_name = serializers.CharField(max_length=50, validators=[MaxLengthValidator(limit_value=50, message="Last name cannot exceed 50 characters.")])

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ["first_name", "last_name"]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        instance.phone = validated_data.get("phone", instance.phone)
        instance.save()
        return instance


class UserSigInSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, min_length=2)
    password = serializers.CharField(max_length=50, min_length=1)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "password"]
        read_only_fields = ("username",)

    def validate(self, data):
        if self.context.get("request") and self.context["request"].method == "POST":
            allowed_keys = set(self.fields.keys())
            input_keys = set(data.keys())
            extra_keys = input_keys - allowed_keys
            if extra_keys:
                raise serializers.ValidationError(f"Additional keys are not allowed: {', '.join(extra_keys)}")
        return data


class UserInformationSerializer(BaseUserSerializer):

    class Meta(BaseUserSerializer.Meta):
        fields = BaseUserSerializer.Meta.fields + ["first_name", "last_name"]
