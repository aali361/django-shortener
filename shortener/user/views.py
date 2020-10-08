from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied, NotAcceptable
from rest_framework.authtoken.models import Token

from . import serializers as usr_serializers
from . import models as usr_models


class SignUpAPIView(APIView):
    serializer_class = usr_serializers.SignUpSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if usr_models.Profile.objects.filter(email=data['email']).first() is not None:
            raise NotAcceptable(detail='email is duplicate')
        if usr_models.Profile.objects.filter(username=data['username']).first() is not None:
            raise NotAcceptable(detail='username is duplicate')
        user = usr_models.Profile.objects.create_user(data['username'], data['email'], data['password'])
        return Response(self.serializer_class(user).data)


class SignInAPIView(APIView):
    serializer_class = usr_serializers.SignInSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if 'username' in data:
            user = authenticate(username=data['username'], password=data['password'])
        elif 'email' in data:
            from .auth import EmailBackend
            user = EmailBackend.authenticate(self, request, email=data['email'], password=data['password'])
        
        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"user": self.serializer_class(user).data, "token": token.key})
        else:
            raise PermissionDenied(detail='wrong authentication information')
