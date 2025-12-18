from rest_framework import serializers

from .models import HeartRate


class WearOSAuthSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    class Meta:
        fields = ("username", "password")


class WearOSTokenSerializer(serializers.Serializer):
    token = serializers.CharField(read_only=True)


class HeartRateSerializer(serializers.ModelSerializer):

    bpm = serializers.IntegerField()
    timestamp = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z")

    class Meta:
        model = HeartRate
        fields = ("bpm", "timestamp")
