from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default="")
    buy_paidcontent = models.BooleanField(default=False, verbose_name='Оплатил контент?')

    def __str__(self):
        return str(self.user)


class Article(models.Model):
    headline = models.CharField(max_length=200, verbose_name='Главная полоса', default="")
    content = models.TextField(verbose_name='Статья', default="")
    image = models.ImageField(upload_to='img/%Y/%m/%d/', height_field=None, width_field=None, max_length=100, verbose_name='ФОТО', default="")
    is_paid = models.BooleanField(default=False, verbose_name='Платный контент')

    def __str__(self):
        return self.headline
