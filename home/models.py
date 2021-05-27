from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Stock(models.Model):
    symbol = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    currency = models.CharField(max_length=500)
    exchangeTimezoneName = models.CharField(max_length=500)
    market = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.symbol


class Portfolio(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    stock = models.ForeignKey(Stock, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.user} - {self.name}'


class Activity(models.Model):
    class Meta:
        verbose_name_plural = 'Activities'
    portfolio = models.ForeignKey(Portfolio, null=True, on_delete=models.SET_NULL)
    BUY_OR_SELL = (
        ('buy', 'buy'),
        ('sell', 'sell')
    )
    bought_or_sold = models.CharField(max_length=50)
    number_stocks = models.IntegerField(null=True)
    price_entered = models.FloatField(null=True)
    date_purchase = models.DateTimeField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return f'{self.portfolio.user} - {self.portfolio} - Activity {self.pk}'
