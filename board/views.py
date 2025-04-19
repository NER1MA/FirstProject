from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post


def home(request):
    return HttpResponse("Hello, Django World!")


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'board/post_list.html', {'posts': posts})


def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Post.objects.create(title=title, content=content)
        return redirect('/')
    return render(request, 'board/post_form.html')


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'board/post_detail.html', {'post': post})


def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect(f'/post/{post_id}/')
    return render(request, 'board/post_form.html', {'post': post})


def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('/')
