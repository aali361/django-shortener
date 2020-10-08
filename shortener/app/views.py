import hashlib

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
        short_url = hashlib.md5('{}{}'.format(request.user.id, data['url']).encode('utf-8')).hexdigest()[:10]
        if 'sug_url' in data:
            short_url = '{}{}'.format(data['sug_url'], short_url)[:10]
        obj, created = app_models.URL.objects.get_or_create(owner=request.user, url=data['url'], short=short_url)
        if not created:
            raise NotAcceptable(detail='please change or set sug_url')
        return Response(app_serializers.URLSerializer(obj).data)
