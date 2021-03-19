from django.db import models

# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=500)
    name = models.CharField(max_length=500)
    currency = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name