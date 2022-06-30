from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('projects/<str:fname>/',views.details, name='details'),
]