from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('details/<str:fname>/',views.details, name='details'),
    path('upload/',views.upload, name='upload'),
    path('list_config/',views.list_config, name='list_config'),
    path('view_config/<str:scheme_name>/',views.view_config, name='view_config'),


]