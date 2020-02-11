"""assist_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from apps.at_auth import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.at_auth.urls')),
    path('accounts/login/', views.login),
    path('purchase_order/', include('apps.purchase_order.urls')),
    path('supplier/', include('apps.supplier.urls')),
    path('product_center/', include('apps.product_center.urls')),
    path('http_tools/', include('apps.http_tools.urls')),
    path('wms_center/', include('apps.wms_center.urls')),
]
