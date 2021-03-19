from django.urls import path
from . import views
from .dash_apps.finished_apps import simpleexample
app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('stock_vis/', views.search_stock, name="stock"),
    # path('show_data/', views.show_data, name='show_data'),
    path('show_stocks/', views.get_stock, name='show_stocks'),
    path('stock/<str:symbol>', views.single_stock, name='show_stock_vis'),
    path('stock_analysis/<str:symbol>/<int:dtime>', views.stockAnalysis, name='stock_analysis'),
]