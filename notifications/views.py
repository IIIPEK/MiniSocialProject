# notifications/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from social.models import Notification

@login_required
def notification_list(request):
    notifications = Notification.objects.filter(recipient=request.user).order_by('-created_at')
    return render(request, 'notifications/notification_list.html', {'notifications': notifications})

@login_required
def mark_all_notifications_read(request):
    Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
    return redirect('notifications:notification_list')

@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
    notification.is_read = True
    notification.save()
    return redirect('notifications:notification_list')
