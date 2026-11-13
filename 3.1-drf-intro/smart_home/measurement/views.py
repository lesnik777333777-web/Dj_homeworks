from rest_framework import generics
from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer, MeasurementCreateSerializer


class SensorListCreateView(generics.ListCreateAPIView):
    """GET: список датчиков, POST: создание нового датчика"""
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer


class SensorRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    """GET: подробная информация о датчике, PATCH/PUT: изменение датчика"""
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer


class MeasurementCreateView(generics.CreateAPIView):
    """POST: добавление нового измерения температуры"""
    queryset = Measurement.objects.all()
    serializer_class = MeasurementCreateSerializer
