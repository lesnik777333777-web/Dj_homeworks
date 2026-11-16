import django_filters
from .models import Advertisement

class AdvertisementFilter(django_filters.rest_framework.FilterSet):
    # Переопределяем только created_at, чтобы использовать диапазон дат
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Advertisement
        fields = ['created_at', 'status']
