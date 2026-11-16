from rest_framework import serializers
from .models import Advertisement, AdvertisementStatusChoices

class AdvertisementSerializer(serializers.ModelSerializer):
    creator = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Advertisement
        fields = ('id', 'title', 'description', 'status', 'creator', 'created_at', 'updated_at')

    def validate(self, attrs):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            is_creating = request.method == 'POST'
            is_updating_to_open = request.method in ('PUT', 'PATCH') and attrs.get('status') == AdvertisementStatusChoices.OPEN

            if is_creating or is_updating_to_open:
                open_ads_count = Advertisement.objects.filter(
                    creator=request.user,
                    status=AdvertisementStatusChoices.OPEN
                ).count()

                # Если обновляем существующее и оно уже было OPEN, не учитываем его в лимите
                if self.instance and self.instance.status == AdvertisementStatusChoices.OPEN:
                    open_ads_count -= 1

                if open_ads_count >= 10:
                    raise serializers.ValidationError("У пользователя не может быть более 10 открытых объявлений.")
        return attrs
