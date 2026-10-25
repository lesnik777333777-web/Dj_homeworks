from django.db import models
from django.utils.text import slugify

class Phone(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="ID")
    name = models.CharField(max_length=255, verbose_name="Название")
    price = models.IntegerField(verbose_name="Цена")
    image = models.URLField(max_length=500, verbose_name="Изображение")
    release_date = models.DateField(verbose_name="Дата выхода")
    lte_exists = models.BooleanField(verbose_name="Поддержка LTE")
    slug = models.SlugField(max_length=255, unique=True, blank=True, verbose_name="URL")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Телефон"
        verbose_name_plural = "Телефоны"
        ordering = ['name']
