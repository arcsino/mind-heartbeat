from rest_framework import serializers

from .models import HeartRate


class HeartRateSerializer(serializers.ModelSerializer):

    bpm = serializers.IntegerField()
    timestamp = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S%z")

    class Meta:
        model = HeartRate
        fields = ("bpm", "timestamp")
