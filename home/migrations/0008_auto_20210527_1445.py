# Generated by Django 3.1.7 on 2021-05-27 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20210527_1430'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Purchase',
            new_name='Activity',
        ),
    ]