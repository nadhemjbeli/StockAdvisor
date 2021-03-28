from django.urls import path
from .views import search_stock, get_stock, single_stock, get_cash_flow, get_income_statements, get_stock_summary, stockAnalysis, home
app_name = 'home'
urlpatterns = [
    path('', home, name='home'),
    path('stock_vis/', search_stock, name="show_stock_vis"),
    # path('show_data/', views.show_data, name='show_data'),
    path('show_stocks/', get_stock, name='show_stocks'),
    path('stock/<str:symbol>', single_stock, name='show_single_stock'),
    path('stock/<str:symbol>/financials', get_income_statements, name='show_financials'),
    path('stock/<str:symbol>/cash_flow', get_cash_flow, name='show_cash_flow'),
    path('stock/<str:symbol>/Summary', get_stock_summary, name='show_summary'),
    path('stock_analysis/<str:symbol>/<int:dtime>', stockAnalysis, name='stock_analysis'),
]