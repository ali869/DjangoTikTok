from .models import Hashtag, StatsData
from rest_framework import serializers


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = "__all__"


class StatsDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatsData
        fields = "__all__"
