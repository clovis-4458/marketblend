from django.shortcuts import render, get_object_or_404
from .models import BlogPost

# ✅ List all blog posts
def blog_list(request):
    posts = BlogPost.objects.all().order_by('-published_date')  # Latest first
    return render(request, 'blog/blog_list.html', {'blog_posts': posts})

# ✅ Show a single blog post
def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, 'blog/blog_detail.html', {'post': post})
