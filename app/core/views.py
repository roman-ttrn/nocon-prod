from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django_ratelimit.decorators import ratelimit
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from user.models import Post
from .forms import PostForm

#@ratelimit(key='ip', rate='5/m', block=True)
@csrf_protect
def main(request):
    if request.user.is_authenticated:
        posts = Post.objects.all().order_by('-created_at')
        if request.method != 'POST':
            form = PostForm()
            return render(request, 'core/main.html', {'posts': posts, 'form': form})
        else:
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user  # 👈 вот это ключ
                post.save()
                return redirect('main')
            else:
                messages.error(request, 'Invalid post form.')
                return render(request, 'core/main.html', {'posts': posts, 'form': PostForm()})

    return redirect('home')

@require_POST
def like_post(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        return JsonResponse({
            'likes': post.total_likes(),
            'status': 'success'
        })
    except Post.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Post not found'
        }, status=404)

@login_required
def delete_post(req, pk):
    post = get_object_or_404(Post, pk=pk)
    if req.user == post.author:
        post.delete()
    return redirect('main')

def certain_post(request, post_id):
    if not request.user.is_authenticated:
        return redirect('home')
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'core/certain_post.html', {'post': post})