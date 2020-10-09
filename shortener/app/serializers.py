from rest_framework import serializers

from . import models as app_models

class ShortenSerializer(serializers.Serializer):
    url = serializers.URLField()
    sug_url = serializers.CharField(max_length=5, required=False)


class URLSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['short']='https://myURLshortener.example.com/r/{}/'.format(instance.short)
        return data

    class Meta:
        model = app_models.URL
        fields = ('url', 'short')


class ReportListSerializer(serializers.ModelSerializer):
    class Meta:
        model = app_models.Report
        fields = ('id', 'url', 'type', 'user_repetitive', 'created_at')


class ReportRetrieveSerializer(serializers.ModelSerializer):
    class Meta:
        model = app_models.Report
        fields = ('id', 'url', 'type', 'user_repetitive', 'view', 'device', 'browser', 'created_at')