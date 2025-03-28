from django.shortcuts import render, redirect
from .models import Notification
from django.contrib import messages
from django.http import HttpResponseRedirect

# Create your views here.

def view_all_notifications(request):
    if request.user.is_authenticated:
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        if not notifications or len(notifications) == 0:
                notif_context = {'notifications': {}, 'user': request.user, 'message': 'No notifications at this moment', "has_notifications": False}
        else:
            notif_context = {'notifications': notifications, 'user': request.user}
        return render(request, 'notifications/all_notifications.html', notif_context)
    else:
        messages.error(request, 'You need to be logged in to view notifications')
        return redirect('login')
    
def delete_notification(request, notif_id):
    notification = Notification.objects.get(id=notif_id)
    if request.user.is_authenticated and request.user == notification.user:
        notification.delete()
        messages.success(request, 'Notification deleted successfully')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        messages.error(request, 'You are not authorized to delete this notification')
        return redirect('all_notifications')