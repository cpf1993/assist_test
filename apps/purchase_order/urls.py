from django.urls import path
from . import views

urlpatterns = [
    path('create_po/', views.po_index, name='po_index'),
    path('singlepo_create/', views.singlepo_create, name='single_create'),
    path('create_bill/', views.bill_index, name='bill_index'),
    path('bill_create/', views.bill_create, name='bill_create'),
    path('po_update/', views.po_update, name='po_update'),
    path('po_log/', views.po_log, name='po_log')
]