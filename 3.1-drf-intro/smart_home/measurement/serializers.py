from rest_framework import serializers
from .models import Sensor, Measurement


class MeasurementSerializer(serializers.ModelSerializer):
    """Сериализатор для отображения измерений внутри датчика (только чтение)"""
    class Meta:
        model = Measurement
        fields = ['temperature', 'created_at', 'image']


class SensorSerializer(serializers.ModelSerializer):
    """Сериализатор для списка датчиков (краткая информация)"""
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description']


class SensorDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для подробной информации о датчике с вложенными измерениями"""
    measurements = MeasurementSerializer(read_only=True, many=True)

    class Meta:
        model = Sensor
        fields = ['id', 'name', 'description', 'measurements']


class MeasurementCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания нового измерения"""
    class Meta:
        model = Measurement
        fields = ['sensor', 'temperature', 'image']
