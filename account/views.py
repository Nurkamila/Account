from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from .serializers import *
from .helpers import send_confirmation_email, send_resetpassword_link

import uuid

User = get_user_model()


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            send_confirmation_email(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class ActivationView(APIView):
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            code = serializer.validated_data['activation_code']
            user = get_object_or_404(get_user_model(), activation_code = code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response({'msg': 'User successfully activated'})


class ResetPasswordEmailView(APIView):
    
    def create_reset_code(self):
        code = str(uuid.uuid4())
        return code
    
    def post(self, request):
        email = request.data['email']
        code = self.create_reset_code()
        ResetPasswordEmailSerializer(data=request.data)
        if User.objects.filter(email=email).exists():
            User.objects.filter(email=email).update(users_reset_code = code)
            send_resetpassword_link(email, code)
        return Response({"msg": "We have sent you a link to reset your password, please check your gmail"})


class ResetPasswordView(APIView):

    def post(self, request, **kwargs):
        serializer = ResetPsswordSerializer(data=request.data)
        code = kwargs['code']
        if serializer.is_valid(raise_exception=True):
            if User.objects.filter(users_reset_code=code).exists():
                serializer.validated_data.pop('confirm_password')
                user = get_object_or_404(get_user_model(), users_reset_code = code)
                password = serializer.validated_data['password']
                user.users_reset_code = ''
                user.password = password
                user.set_password(password)
                user.save()
                return Response({'msg': "Life is good when everything is good"})
            return Response({'msg': 'Not a valid link'}, status=status.HTTP_404_NOT_FOUND)