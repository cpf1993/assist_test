from django.urls import path
from apps.wms_center import views

urlpatterns = [
    path('gip_search/', views.gip_search, name='gip_search'),
    path('search_result/', views.get_gip_info, name='get_gip_info'),
    path('bind_idlesku/', views.bind_idleSku, name='bind_idlesku'),
    path('confirm_bind/', views.confirm_bind, name='confirm_bind'),
    path('operate_guide/', views.operateGuide, name='operateGuide'),
    path('get_dailycargoplan/', views.get_dailyCargoPlan, name='get_dailyCargoPlan'),
    path('get_dailyCgPlanResult/', views.get_dailycgPlanResult, name='get_dailyCgPlanResult'),
    # path('editDailyCargoPlan/',views.editDailyCargoPlan,name = 'editDailyCargoPlan'),
    path('getDailyCgPlanById/', views.getDailyCgPlanById, name='getDailyCgPlanById'),
    path('editDailyCgPlan/', views.editDailyCgPlan, name='editDailyCgPlan'),
    path('pda_operate_shelve/', views.pda_operate_shelve, name='pda_operate_shelve'),
    path('operate_shelve_tool/', views.operate_shelve_tool, name='operate_shelve_tool'),
    path('time_task/', views.time_task, name='time_task'),
    path('celery_task/', views.celery_task, name='celery_task'),
]

