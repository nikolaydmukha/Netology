from django.db import models

# Create your models here.


class Phone(models.Model):
    name = models.CharField(u'Название', max_length=64)
    vendor = models.CharField(u'Производитель', max_length=64)
    devicetype = models.CharField(u'Тип', max_length=64)
    os = models.CharField(u'ОС', max_length=64)
    ram = models.IntegerField(u'Память')
    price = models.IntegerField(u'Цена')
    cam = models.IntegerField(u'Камера')
    weight = models.IntegerField(u'Вес')
    display = models.IntegerField(u'Диагональ дисплея')

    def __str__(self):
        return '%s' % self.name


class Iphone(models.Model):
    #name = models.CharField(u'Название', max_length=64)
    name = models.OneToOneField(Phone, on_delete=models.CASCADE, primary_key=True)
    faceid = models.CharField(u'Face id', max_length=64)
    applepay = models.CharField(u'Apple pay', max_length=64)

    def __str__(self):
        return '%s' % self.name


class Samsung(models.Model):
    #name = models.CharField(u'Название', max_length=64)
    name = models.OneToOneField(Phone, on_delete=models.CASCADE, primary_key=True)
    fm = models.CharField(u'Радио', max_length=64)
    samsungpay = models.CharField(u'Samsung pay', max_length=64)
    ikport = models.CharField(u'ИК-порт', max_length=64)

    def __str__(self):
        return '%s' % self.name
