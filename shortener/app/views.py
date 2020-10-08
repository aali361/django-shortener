from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotAcceptable

from . import serializers as app_serializers
from . import models as app_models


class ShortenAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = app_serializers.ShortenSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        return Response({})
