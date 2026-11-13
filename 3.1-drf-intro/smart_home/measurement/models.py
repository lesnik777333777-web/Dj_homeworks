from django.db import models

class Sensor(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название")
    description = models.TextField(null=True, blank=True, verbose_name="Описание")

    def __str__(self):
        return self.name


class Measurement(models.Model):
    sensor = models.ForeignKey(
        Sensor,
        related_name='measurements',
        on_delete=models.CASCADE,
        verbose_name="Датчик"
    )
    temperature = models.FloatField(verbose_name="Температура")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата и время измерения")

    # Дополнительное задание: необязательное поле для изображения
    image = models.ImageField(null=True, blank=True, upload_to='measurements/', verbose_name="Изображение")

    def __str__(self):
        return f"Измерение {self.temperature}°C для {self.sensor.name} ({self.created_at})"
