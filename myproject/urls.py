"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from board import views
from django.shortcuts import redirect
from board.views import PostListCreateAPIView, PostDeleteAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('/board/')),  # Redirect root URL to login page
    path('', include('account.urls')),
    path('board/', include('board.urls')),
    path('write/', views.post_create),
    path('post/<int:post_id>/', views.post_detail),
    path('post/<int:post_id>/edit/', views.post_edit),
    path('post/<int:post_id>/delete/', views.post_delete),
    path('comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
    path('board/api/posts/', PostListCreateAPIView.as_view(), name='api_post_list_create'),
    path('api/posts/', PostListCreateAPIView.as_view(), name='api_post_list_create_direct'),
    path('api/posts/<int:id>/delete/', PostDeleteAPIView.as_view(), name='post_delete_api'),
]
