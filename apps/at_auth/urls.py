from django.urls import path
from . import views

urlpatterns = [
    path('forget_password/', views.forget_password, name='forget_password'),
    path('login/', views.login, name='login'),
    path('login_action/', views.login_action, name='login_action'),
    path('index/', views.index, name='index'),
    path('logout/', views.logout, name='logout'),
    path('check_health/', views.check_health),
]