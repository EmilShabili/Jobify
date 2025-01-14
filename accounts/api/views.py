from .serializers import (
    LoginSerializer, RegisterSerializer, ActivationSerializer, CheckEmailSerializer, ChangePasswordSerializer,
    ResetPasswordCompleteSerializer)
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str

User = get_user_model()


class LoginView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = LoginSerializer


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ActivationView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ActivationSerializer
    lookup_field = "uuid"

    def get_object(self):
        uuid = self.kwargs.get(self.lookup_field)
        id_ = smart_str(urlsafe_base64_decode(uuid))
        return User.objects.get(id=int(id_))

    def put(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, instance=self.get_object())
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class ResetPasswordView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CheckEmailSerializer


class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = ChangePasswordSerializer

    def get_object(self):
        return self.request.user


class ResetPasswordCompleteView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ResetPasswordCompleteSerializer
    lookup_field = 'uuid'

    def get_object(self):
        uuid = self.kwargs.get(self.lookup_field)
        id_ = smart_str(urlsafe_base64_decode(uuid))
        return User.objects.get(id=id_)
