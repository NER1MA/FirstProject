from django.urls import path
from board.views import CommentListAPIView, CommentCreateAPIView, PostListCreateAPIView
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('api/posts/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('api/comments/<int:post_id>/', CommentListAPIView.as_view(), name='comment-list'),
    path('api/comments/create/', CommentCreateAPIView.as_view(), name='comment-create'),
]
