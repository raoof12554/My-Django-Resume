# C:\Users\admin\Desktop\resume_proje_django\djangoProject\my_team\urls.py

from django.urls import path
from . import views

app_name = 'my_team'

urlpatterns = [
    # فرض می‌کنیم شما یک صفحه جداگانه برای نمایش لیست کامل اعضای تیم دارید
    path('', views.team_list_view, name='team_list'), # نام team_list را برای این مسیر در نظر گرفتیم
]