# Generated by Django 3.1.7 on 2021-06-24 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20210624_2217'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='image',
        ),
    ]
