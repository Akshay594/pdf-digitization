from rest_framework import serializers
from .models import ConsumerData


class DataSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=20)
    data = serializers.CharField(max_length=20000)

    def create(self, validated_data):
        return ConsumerData.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.tite = validated_data.get('title', instance.title)
        instance.data = validated_data.get('data', instance.data)
        instance.save()
        return instance