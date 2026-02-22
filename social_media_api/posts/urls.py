from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet

router = DefaultRouter()
router.register(r'posts', PostViewSet)      # generates /posts/, /posts/<id>/
router.register(r'comments', CommentViewSet)  # generates /comments/, /comments/<id>/

urlpatterns = [
    path('', include(router.urls)),
]

from .views import user_feed

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', user_feed),
]