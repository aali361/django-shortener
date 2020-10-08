from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied

from shortener.auth import EmainAuthetication
from . import serializers as usr_serializers


class SignUpAPIView(APIView):
    serializer_class = usr_serializers.SignUpSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        user = User.objects.create_user(data['username'], data['email'], data['password'])
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
            user = EmainAuthetication.authenticate(self, request, username=data['email'], password=data['password'])
        
        print(user.password)
        print(make_password(data['password']))
        
        if user is not None:
            return Response(self.serializer_class(user).data)
        else:
            raise PermissionDenied(detail='wrong authentication information')
