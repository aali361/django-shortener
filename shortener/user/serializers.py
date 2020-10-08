from rest_framework import serializers

class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(max_length=300)
    password = serializers.CharField(max_length=300, write_only=True)


class SignInSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    username = serializers.CharField(max_length=300, required=False)
    password = serializers.CharField(max_length=300, write_only=True)
