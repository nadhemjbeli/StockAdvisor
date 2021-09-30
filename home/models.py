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


class Transaction(models.Model):
    # class Meta:
    #     verbose_name_plural = 'Activities'
    portfolio = models.ForeignKey(Portfolio, null=True, on_delete=models.SET_NULL)

    number_stocks = models.IntegerField(null=True)
    buying_price = models.FloatField(null=True)
    date_to_buy = models.DateTimeField(null=True)
    selling_price = models.FloatField(null=True)
    date_to_sell = models.DateTimeField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.portfolio} - Transaction {self.pk}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user.username} Profile'

import datetime as dt
class News(models.Model):
    class Meta:
        verbose_name_plural = 'News'

    # portfolio = models.ForeignKey(Portfolio, null=True, on_delete=models.SET_NULL)
    stock = models.ForeignKey(Stock, null=True, on_delete=models.SET_NULL)

    title = models.TextField()
    source = models.CharField(max_length=500)
    description = models.TextField()
    link = models.CharField(max_length=500)
    date_article = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'{self.stock.symbol} - News {self.pk} - {self.date_article.strftime("%Y-%m-%d")}'
