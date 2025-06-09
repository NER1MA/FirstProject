from rest_framework import generics
from .serializers import PostSerializer
from .serializers import CommentSerializer
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post
from .models import Comment
from .forms import CommentForm
from rest_framework.permissions import AllowAny


def home(request):
    return HttpResponse("Hello, Django World!")


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'board/post_list.html', {'posts': posts})



@login_required
def post_create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        Post.objects.create(title=title, content=content, author=request.user)
        return redirect('/board/')
    return render(request, 'board/post_form.html')


def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all().order_by('-created_at')

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.author = request.user
            comment.save()
            return redirect(f'/post/{post_id}/')
    else:
        form = CommentForm()

    return render(request, 'board/post_detail.html', {
        'post': post,
        'comments': comments,
        'form': form
    })

@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect(f'/post/{post_id}/')
    return render(request, 'board/post_form.html', {'post': post})

@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('/board/')

@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    post_id = comment.post.id
    if request.method == 'POST':
        comment.delete()
        return redirect(f'/post/{post_id}/')
    return redirect('/')


# REST API view for listing and creating posts
class PostListCreateAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}


# REST API view for creating comments
class CommentCreateAPIView(generics.CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_serializer_context(self):
        return {'request': self.request}

    def perform_create(self, serializer):
        request = self.request
        post_id = request.data.get('post')
        if request.user.is_authenticated:
            serializer.save(author=request.user, post_id=post_id)
        else:
            author_name = request.data.get('author', '익명')
            serializer.save(author=author_name, post_id=post_id)

class CommentListAPIView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id).order_by('-created_at')