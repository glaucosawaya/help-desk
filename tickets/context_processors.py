from .models import Notification


def notifications(request):

    if request.user.is_authenticated:

        unread_notifications = Notification.objects.filter(
            recipient=request.user,
            is_read=False
        )

        unread_count = unread_notifications.count()

        recent_notifications = unread_notifications[:5]

        return {
            "unread_notifications_count": unread_count,
            "recent_notifications": recent_notifications,
        }

    return {
        "unread_notifications_count": 0,
        "recent_notifications": [],
    }
