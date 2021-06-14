from django.contrib import admin
from .models import Stock, Portfolio, Transaction, Profile

# Register your models here.


admin.site.register(Stock)
admin.site.register(Portfolio)
admin.site.register(Transaction)
admin.site.register(Profile)