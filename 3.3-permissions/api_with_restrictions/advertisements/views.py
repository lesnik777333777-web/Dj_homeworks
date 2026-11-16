from rest_framework import viewsets, permissions, filters as drf_filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from django_filters.rest_framework import DjangoFilterBackend

from .models import Advertisement, AdvertisementStatusChoices
from .serializers import AdvertisementSerializer
from .filters import AdvertisementFilter
from .permissions import IsAuthorOrAdminOrReadOnly

class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend, drf_filters.SearchFilter, drf_filters.OrderingFilter]
    filterset_class = AdvertisementFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'updated_at']

    def get_permissions(self):
        # Для создания нужна строгая авторизация
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated]
        else:
            # Для просмотра, обновления, удаления используем наш кастомный класс
            permission_classes = [IsAuthorOrAdminOrReadOnly]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Дополнительное задание: DRAFT виден только автору и админу.
        """
        user = self.request.user
        if user.is_authenticated:
            # Пользователь видит свои объявления (любые статусы) + чужие НЕ черновики
            return Advertisement.objects.filter(
                models.Q(creator=user) | ~models.Q(status=AdvertisementStatusChoices.DRAFT)
            )
        # Неавторизованный пользователь видит только не-черновики
        return Advertisement.objects.exclude(status=AdvertisementStatusChoices.DRAFT)

    # Дополнительное задание: Избранное (добавить/удалить)
    @action(detail=True, methods=['post', 'delete'], permission_classes=[permissions.IsAuthenticated])
    def favorite(self, request, pk=None):
        advertisement = self.get_object()

        if advertisement.creator == request.user:
            return Response({"error": "Автор не может добавить свое объявление в избранное"}, status=400)

        if request.method == 'POST':
            advertisement.favorites.add(request.user)
            return Response({"status": "added to favorites"})
        elif request.method == 'DELETE':
            advertisement.favorites.remove(request.user)
            return Response({"status": "removed from favorites"})

    # Дополнительное задание: Фильтрация по избранным объявлениям пользователя
    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def my_favorites(self, request):
        queryset = self.get_queryset().filter(favorites=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
