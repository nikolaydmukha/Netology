# Generated by Django 2.2 on 2019-06-28 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reporter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(default='', max_length=70, verbose_name='Имя репортёра')),
            ],
        ),
        migrations.AddField(
            model_name='article',
            name='content',
            field=models.TextField(default='', verbose_name='Статья'),
        ),
        migrations.AddField(
            model_name='article',
            name='headline',
            field=models.CharField(default='', max_length=200, verbose_name='Главная полоса'),
        ),
        migrations.AddField(
            model_name='article',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Платный контент'),
        ),
        migrations.AddField(
            model_name='profile',
            name='buy_paidcontent',
            field=models.BooleanField(default=False, verbose_name='Оплатил контент?'),
        ),
        migrations.AddField(
            model_name='profile',
            name='full_name',
            field=models.CharField(default='', max_length=70, verbose_name='Имя пользователя'),
        ),
        migrations.AddField(
            model_name='article',
            name='reporter',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='articles.Reporter', verbose_name='Репортёр'),
        ),
    ]
