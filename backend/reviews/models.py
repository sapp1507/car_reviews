from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Q, F

from .validators import year_validator

User = get_user_model()


class Country(models.Model):
    """Страна производителя автомобиля"""
    name = models.CharField(max_length=255, verbose_name='Имя', unique=True)

    class Meta:
        verbose_name = 'Страна'
        verbose_name_plural = 'Страны'
        ordering = ['name']

    def __str__(self):
        return self.name


class Brand(models.Model):
    """Производитель автомобиля"""
    name = models.CharField(max_length=255, verbose_name='Имя', unique=True)
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        verbose_name='Страна',
        related_name='brands',
        null=True
    )

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'
        ordering = ['name']

    def __str__(self):
        return self.name


class CarModel(models.Model):
    """Модель автомобиля"""
    name = models.CharField(max_length=255, verbose_name='Имя')
    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        verbose_name='Автомобиль',
        related_name='brands'
    )
    year_release = models.IntegerField(
        verbose_name='год начала выпуска',
        validators=[year_validator]
    )
    year_completion = models.IntegerField(
        verbose_name='Год окончания выпуска',
        validators=[year_validator]
    )

    class Meta:
        verbose_name = 'Модель автомобиля'
        verbose_name_plural = 'Модели автомобилей'
        ordering = ['name']

        constraints = [
            models.CheckConstraint(
                check=Q(year_release__gt=F('year_completion')),
                name='release_year_to_big')
        ]

    def __str__(self):
        return self.name


class Comment(models.Model):
    """Комментарий к автомобилю"""
    author = models.ForeignKey(
        User,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    car_model = models.ForeignKey(
        CarModel,
        related_name='comments',
        on_delete=models.CASCADE,
        verbose_name='Модель автомобиля'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    text = models.TextField(verbose_name='Комментарий')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-pub_date']

    def __str__(self):
        return self.text[:20]
