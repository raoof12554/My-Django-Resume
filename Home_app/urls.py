# Home_app/urls.py

from django.urls import path
from . import views

app_name = 'home_app' 

urlpatterns = [
    path('', views.home_view, name='home'), 
    path('about/', views.about_view, name='about'), 
    path('services/', views.services_view, name='services'), 
    path('portfolio/<int:pk>/', views.portfolio_detail_view, name='portfolio_detail'), 
    path('skills/', views.skills_view, name='skills'), 
    
]