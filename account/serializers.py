from email.message import EmailMessage
from rest_framework.serializers import ModelSerializer, CharField, Serializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.forms import ValidationError
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class RegisterSerializer(ModelSerializer):
    inn = CharField(required=True, write_only=True, min_length=True)
    password = CharField(min_length=6, required=True, write_only=True)
    
    
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'sex', 'inn', 'email', 'password')

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError('User with this email already exists')
        return value


    def validate(self, validated_data):
        sex = validated_data.get('sex')
        inn = validated_data.get('inn')
        if not str(inn).isdigit():
            raise ValidationError('INN must be number')
        elif sex == 'f':
            if not str(inn).startswith('1'):
                raise ValidationError('INN must start with 1')
        else:
            if not str(inn).startswith('2'):
                raise ValidationError('INN must start with 2')
        return validated_data


    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    pass


class ActivationSerializer(Serializer):
    activation_code = CharField(required=True, write_only=True, max_length=255)


class ResetPasswordEmailSerializer(ModelSerializer):
    email = EmailMessage


class ResetPsswordSerializer(ModelSerializer):
    password = CharField(min_length=6, required=True, write_only=True)
    confirm_password = CharField(min_length=6, required=True, write_only=True)

    class Meta:
        model = User
        fields = ('password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] == attrs['confirm_password']:
            return attrs
        else:
            raise ValidationError({"error": "Passwords don't match. Please try again!"})