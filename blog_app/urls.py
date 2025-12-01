# blog_app/urls.py

from django.urls import path
from . import views

app_name = 'blog_app' # <--- حتماً این namespace را تعریف کنید

urlpatterns = [
    path('', views.blogs_list_view, name='blogs_list'),
    path('<int:pk>/', views.blog_detail_view, name='blog_detail'),
    # اگر ویوهای دیگری دارید، اینجا اضافه کنید
]