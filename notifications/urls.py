from django.urls import path, include
from . import views

urlpatterns = [
    path('all/', views.view_all_notifications, name='all_notifications'),
    path('delete/<int:notif_id>/', views.delete_notification, name='delete_notification'),
]