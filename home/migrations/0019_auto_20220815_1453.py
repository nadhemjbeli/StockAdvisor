# Generated by Django 3.1.7 on 2022-08-15 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20210624_2247'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='date_article',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]