# Generated by Django 3.1.7 on 2021-05-27 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_auto_20210527_1445'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity',
            options={'verbose_name_plural': 'Activities'},
        ),
        migrations.RenameField(
            model_name='activity',
            old_name='date_purchase',
            new_name='date_activity',
        ),
    ]
