from django.urls import path
from board.views import *
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('api/posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('api/comments/<int:post_id>/', CommentListAPIView.as_view(), name='comment-list'),
    path('api/comments/create/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('api/posts/<int:id>/edit/', PostUpdateAPIView.as_view(), name='post_edit_api'),
]
