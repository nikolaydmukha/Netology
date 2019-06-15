from django.db import models


class Phone(models.Model):
    name = models.CharField(u'Название', max_length=64)
    price = models.IntegerField(u'Цена')
    image = models.CharField(u'Изоюражение', max_length=128)
    release_date = models.DateField(u'Дата релиза')
    lte_exists = models.BooleanField(u'LTE')
    slug = models.CharField(u'Название', max_length=64)

    def __str__(self):
        return '%s' % self.name