# Generated by Django 2.2 on 2019-06-29 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20190629_2205'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='is_active',
            new_name='isActive',
        ),
    ]
