# Generated by Django 2.2 on 2019-06-28 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20190628_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(default='', upload_to='images', verbose_name='ФОТО'),
        ),
    ]
