# Generated by Django 3.1.7 on 2021-05-27 17:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_auto_20210527_1524'),
    ]

    operations = [
        migrations.RenameField(
            model_name='activity',
            old_name='bought_or_sold',
            new_name='type_activity',
        ),
    ]
