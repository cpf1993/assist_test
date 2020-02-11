from django.urls import path
from . import views

urlpatterns = [
    path('create_ka_data/', views.data_create, name='data_create'),
    path('add_tags/', views.add_tags, name='add_tag'),
    path('query_product/', views.query_product, name='query_product'),
]