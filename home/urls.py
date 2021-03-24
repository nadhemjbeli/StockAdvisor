from django.urls import path
from . import views
from .dash_apps.finished_apps.simpleexample import get_stock, single_stock, search_stock, get_stock_summary
app_name = 'home'
urlpatterns = [
    path('', views.home, name='home'),
    path('stock_vis/', search_stock, name="stock"),
    # path('show_data/', views.show_data, name='show_data'),
    path('show_stocks/', get_stock, name='show_stocks'),
    path('stock/<str:symbol>', single_stock, name='show_stock_vis'),
    path('stock/<str:symbol>/financials', views.get_income_statements, name='show_financials'),
    path('stock/<str:symbol>/Summary', views.get_stock_summary, name='show_summary'),
    path('stock_analysis/<str:symbol>/<int:dtime>', views.stockAnalysis, name='stock_analysis'),
]