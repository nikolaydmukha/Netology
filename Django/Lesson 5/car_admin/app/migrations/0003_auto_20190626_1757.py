# Generated by Django 2.1.1 on 2019-06-26 17:57

import app.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_review_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarsReviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('car', models.CharField(max_length=64, verbose_name=app.models.Review)),
            ],
        ),
        migrations.AlterField(
            model_name='car',
            name='brand',
            field=models.CharField(max_length=50, verbose_name='Марка'),
        ),
        migrations.AlterField(
            model_name='car',
            name='model',
            field=models.CharField(max_length=50, verbose_name='Модель'),
        ),
        migrations.AlterField(
            model_name='review',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Car', verbose_name='Машина'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(verbose_name='Обзор'),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Заголовок'),
        ),
    ]
