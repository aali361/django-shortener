from rest_framework import serializers

from . import models as app_models

class ShortenSerializer(serializers.Serializer):
    url = serializers.URLField()
    sug_url = serializers.CharField(max_length=5, required=False)

class URLSerializer(serializers.ModelSerializer):

    class Meta:
        model = app_models.URL
        fields = ('url', 'short')