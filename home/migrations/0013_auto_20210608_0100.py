# Generated by Django 3.1.7 on 2021-06-08 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0012_auto_20210608_0029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.png', upload_to='profile_pics'),
        ),
    ]
