from django.urls import path
from . import views

urlpatterns = [
    path('', views.view_industries, name='view_industries'),
]