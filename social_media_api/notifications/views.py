from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    notifications = Notification.objects.filter(
        recipient=request.user
    ).order_by('-timestamp')
    
    data = [
        {
            'id': n.id,
            'actor': n.actor.username,
            'verb': n.verb,
            'is_read': n.is_read,
            'timestamp': n.timestamp,
        }
        for n in notifications
    ]
    
    # mark all as read after fetching
    notifications.update(is_read=True)
    
    return Response(data)