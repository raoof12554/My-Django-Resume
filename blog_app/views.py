# blog_app/views.py
from django.shortcuts import render, get_object_or_404
# from .models import BlogPost # اگر مدل BlogPost دارید، آن را ایمپورت کنید

def blogs_list_view(request):
    # posts = BlogPost.objects.all() # اگر BlogPost دارید
    context = {
        # 'posts': posts
    }
    return render(request, 'blog_app/blogs_list.html', context) # <--- این تمپلیت را ایجاد کنید

def blog_detail_view(request, pk):
    # post = get_object_or_404(BlogPost, pk=pk) # اگر BlogPost دارید
    context = {
        # 'post': post
    }
    return render(request, 'blog_app/blog_detail.html', context) # <--- این تمپلیت را ایجاد کنید