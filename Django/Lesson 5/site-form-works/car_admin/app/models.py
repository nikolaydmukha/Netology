from django.db import models


class Car(models.Model):
    brand = models.CharField(max_length=50, verbose_name='Марка')
    model = models.CharField(max_length=50, verbose_name='Модель')

    def __str__(self):
        return f'{self.brand} {self.model}'

    class Meta:
        verbose_name = 'Автомобиль'
        verbose_name_plural = 'Автомобили'

    def review_count(self):
        return Review.objects.filter(car=self).count()

    def get_reviews(self):
        return self.review_count()

    get_reviews.short_description = "Всего отзывов"


class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name='Машина')
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Обзор')

    def __str__(self):
        return str(self.car) + ' ' + self.title

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

