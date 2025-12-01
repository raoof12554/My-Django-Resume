# C:\Users\admin\Desktop\resume_proje_django\djangoProject\contact_app\urls.py

from django.urls import path
from . import views

app_name = 'contact_app'

urlpatterns = [
    path('', views.contact_view, name='contact'),
]