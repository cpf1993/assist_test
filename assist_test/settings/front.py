# encoding: utf-8

# 用于压缩和收集前端数据的配置

from .base import *

CACHES = {
    "default": {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
    "inmem": {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}
