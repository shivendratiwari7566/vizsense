"""VideoAnalyticsPlatformApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from AnalyticsPlatformApi import views

from AnalyticsPlatformApi.device_views import * 
from rest_framework.routers import DefaultRouter
router = DefaultRouter()



router.register(r'api/devices', DeviceViewSet, basename='device')
router.register(r'api/models/development', ModelsViewSet , basename='models-development')
# router.register(r'api/cycle/training', CycleTrainingViewSet , basename='cycle-training')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view ),
    path('api/test_views', views.test_views),
    path('api/functions/create', views.function_create),
    path('api/functions/getFunctions', views.functions_get),
    path('api/functions/details', views.functions_getDetails),
    path('api/functions/getParameters', views.function_getparameters),
    path('api/functions/delete', views.functions_delete),
    path('api/functions/update', views.function_update),
    path('api/sources/create', views.sources_create),
    path('api/sources/getSources', views.sources_get),
    path('api/sources/details', views.sources_details),
    path('api/sources/delete', views.sources_delete),
    path('api/sources/getSubSourceItems',views.getSubSourceItems),
    path('api/sources/getLiveSourceCameras', views.getLiveSourceCameras),
    path('api/sources/getSubSources', views.getSubSources),
    path('api/sources/update',views.sources_update),
    path('api/groups/create', views.groups_create),
    path('api/groups/getGroups', views.groups_get),
    path('api/jobs/create', views.jobs_create),
    path('api/jobs/getJobs', views.jobs_get),
    path('api/jobs/details', views.jobs_detailes),
    path('api/jobs/delete', views.jobs_delete),
    path('api/jobs/update', views.jobs_update),
    path('api/jobs/viewJob', views.viewJob),
    path('api/jobs/getJobAnalytics', views.analytics_tab),
    path('api/operations/create', views.operations_create),
    path('api/misc/getOperationTypes', views.operations_get),
    path('api/tasks/create', views.task_create),
    path('api/misc/getTaskTypes', views.task_get),
    path('api/models/create', views.models_create),
    path('api/models/details',views.models_detailes),
    path('api/models/update',views.models_update),
    path('api/models/delete',views.models_delete),
    path('api/models/getModels', views.models_get),
    path('api/Model_labels/create', views.Model_labels_create),
    path('api/models/getLabels', views.labels_get),
    path('api/cameras/create', views.cameras_create),
    path('api/cameras/getCameras', views.cameras_get),

    path('',include((router.urls, 'app'), namespace='devices')),


     
     

]
