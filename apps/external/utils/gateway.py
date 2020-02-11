# coding=utf-8
import os

from django.conf import settings
from thrift_client.client.rest_client import RestClient


def get_env():
    _env = os.environ['DJANGO_SETTINGS_MODULE'].split('.')[-1]
    if _env.startswith('dev'):
        if settings.WAREHOUSE_SITE == "CHINA":
            return "dev", 'default'
    elif _env.startswith('test'):
        if settings.WAREHOUSE_SITE == "CHINA":
            return "test", 'aliyun-hangzhou'
    elif _env.startswith('pre'):
        if settings.WAREHOUSE_SITE == "CHINA":
            return "pre", 'aliyun-hangzhou'
    elif _env.startswith('prod'):
        if settings.WAREHOUSE_SITE == "CHINA":
            return "prod", "aliyun-hangzhou"
        elif settings.WAREHOUSE_SITE == "INDIA":
            return "prod", "aliyun-india"

    return None, None


class Gateway(object):

    @classmethod
    def client(cls):
        if not hasattr(cls, "_client"):
            env, cluster = get_env()
            if not env:
                raise Exception("网关接口调用失败：获取环境配置失败！")
            cls._client = RestClient(
                env=env,
                cluster=cluster,
                log_dictionary=settings.LOG_ROOT + '/thrift_client.log',
                appliaction="Assist_test-python-rest-client")
        return cls._client

    @classmethod
    def request(cls, url, data=None, timeout=20, project_env=None):
        params = {
            "timeout": timeout
        }
        if data is not None:
            params["json"] = data
        if project_env is not None:
            params["project_env"] = project_env
        res = cls.client()._request(url, **params)
        return res

if __name__ == '__main__':
    get_env()