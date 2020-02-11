# coding=utf-8
from django.urls import path, re_path

from . import views

urlpatterns = [
    # 项目列表
    re_path(r'^project/list/$',
         views.ProjectViewSet.as_view({'get': 'list'}),
         name='project'),
    # 新增项目
    path('project/create/',
         views.ProjectViewSet.as_view({'post': 'create'}),
         name='project'),
    # 获取项目描述
    re_path(r'^project/retrieve/(?P<pk>[0-9]+)/$',
            views.ProjectViewSet.as_view({'get': 'retrieve'}),
            name='project'),
    # 修改项目相关
    re_path(r'^project/update/(?P<pk>[0-9]+)/$',
            views.ProjectViewSet.as_view({'post': 'update'}),
            name='project'),
    # 删除某个项目
    re_path(r'^project/destroy/(?P<pk>[0-9]+)/$',
            views.ProjectViewSet.as_view({'post': 'destroy'}),
            name='project'),

    # 接口列表
    re_path(r'^interface/list/$',
         views.HttpInterfaceViewSet.as_view({'get': 'list'}),
         name='interface'),

    # 新增接口（工具）
    path('interface/create/',
         views.HttpInterfaceViewSet.as_view({'post': 'create'}),
         name='interface'),

    # 获取接口详情
    re_path(r'^interface/basic_info/',
            views.HttpInterfaceBasicInfoView.as_view(),
            name='interface'),

    # 更改接口内容
    re_path(r'^interface/update/(?P<pk>[0-9]+)/$',
            views.HttpInterfaceViewSet.as_view({'post': 'update'}),
            name='interface'),

    # 删除接口
    re_path(r'^interface/destroy/(?P<pk>[0-9]+)/$',
            views.HttpInterfaceViewSet.as_view({'post': 'destroy'}),
            name='interface'),

    # 返回项目和接口关系
    path('interface_of_project/list/',
         views.ProjectAndInterfaceViewSet.as_view({'get': 'list'}),
         name='interface_of_project'),

    # 通过id获取数据库数据直接运行接口
    re_path(r'^interface/run_by_id/$',
            views.RunInterfaceByIdViewSet.as_view(),
            name = "run_interface_by_id"),

    # 通过页面入参，运行接口并返回
    re_path(r'^interface/run_by_input/$',
            views.RunInterfaceByInputViewSet.as_view(),
            name = "run_interface_by_input")
]
