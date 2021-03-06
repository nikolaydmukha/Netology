# Generated by Django 2.2.2 on 2019-06-23 06:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20190623_0527'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='cupboard',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_cupboard', to='books.Cupboard', verbose_name='Шкаф'),
        ),
        migrations.AlterField(
            model_name='books',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_place', to='books.ShelfPlace', verbose_name='Место на полке'),
        ),
        migrations.AlterField(
            model_name='books',
            name='shelf',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_shelf', to='books.Shelf', verbose_name='Полка'),
        ),
    ]
