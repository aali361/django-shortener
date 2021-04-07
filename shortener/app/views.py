import hashlib
from django.utils import timezone
from django.core.cache import cache
from django.shortcuts import get_object_or_404, redirect
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination

from . import models as app_models
from . import serializers as app_serializers
from . import tasks as app_tasks


class ReportPagination(PageNumberPagination):
    page_size = 10


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
        url, _ = app_models.URL.objects.get_or_create(owner=request.user, url=data['url'], 
                            short='{}'.format(short_url))
        return Response(app_serializers.URLSerializer(url).data)


class URLAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, short):
        red_url = cache.get(short)
        app_tasks.register_access.delay(short, request.user.id, request.user_agent.is_mobile,
                                        request.user_agent.is_pc, request.user_agent.browser.family)
        if red_url is None:
            url = get_object_or_404(app_models.URL, short=short)
            red_url = url.url
            cache.set(short, red_url, 10*60)
        return Response({'url':red_url})


class TodayReportAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, url_id):
        url = get_object_or_404(app_models.URL, id=url_id, owner=request.user)
        accesses = app_models.Access.objects.filter(url=url, created_at__date=timezone.now().date())
        statics = app_tasks.get_statics(data=accesses)
        return Response(statics)


class ReportViewSet(ReadOnlyModelViewSet):
    permission_classes = (IsAuthenticated,)
    pagination_class = ReportPagination

    serializers = {
        'list': app_serializers.ReportListSerializer,
        'retrieve': app_serializers.ReportRetrieveSerializer,
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action)

    def get_queryset(self):
        return app_models.Report.objects.filter(url__owner=self.request.user).order_by('id')
