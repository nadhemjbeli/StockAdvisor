# Generated by Django 3.1.7 on 2021-05-27 13:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20210515_0257'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bought_or_sold', models.CharField(max_length=50)),
                ('number_stocks', models.IntegerField(null=True)),
                ('price_entered', models.FloatField(null=True)),
                ('date_purchase', models.DateTimeField(null=True)),
                ('timestamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('portfolio', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.portfolio')),
            ],
        ),
    ]
