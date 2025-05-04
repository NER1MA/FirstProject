from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),  # 게시글 목록 페이지
    path('api/posts/', views.PostListCreateAPIView.as_view(), name='api_post_list_create'),
]
