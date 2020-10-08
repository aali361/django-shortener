from rest_framework import serializers

class ShortenSerializer(serializers.Serializer):
    main_url = serializers.URLField()
    sugg_url = serializers.CharField(max_length=500, required=False)
