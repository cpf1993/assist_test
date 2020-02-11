from django.urls import path
from . import views

urlpatterns = [
    path('log_search/', views.log_search,name='log_search'),
    path('search_result/', views.search_result, name='search_result')
]