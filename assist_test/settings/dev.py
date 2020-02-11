# coding=utf-8

from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'assist_test',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        # 数据库连接设置为MySQL严格模式，防止migrate时警告
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    },
    'assist_test': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'assist_test',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        # 数据库连接设置为MySQL严格模式，防止migrate时警告
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    },
    'purchase': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    },
    'supplier_mgr': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    },
    'odoo_dev': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    },

    'idoo_all': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    },
    'idoo_hangzhou2': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    },
    'idoo_dongguan2': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        }
    },
}

DATABASE_APPS_MAPPING = {
    'contenttypes': 'default',
    'auth': 'default',
    'admin': 'default',
    'sessions': 'default',
    'messages': 'default',
    'staticfiles': 'default',
    'at_auth': 'default',
    'purchase_order': 'purchase',
    'supplier': 'supplier_mgr',
    'product_center': 'odoo_dev',
    'http_tools': 'assist_test',
}

WAREHOUSE_SITE = "CHINA"  # 站点
