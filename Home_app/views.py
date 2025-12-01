# C:\Users\admin\Desktop\resume_proje_django\djangoProject\Home_app\views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
import logging

from contact_app.forms import ContactForm
from contact_app.models import Message

from my_team.models import TeamMember 
from .models import PortfolioCategory, PortfolioPage, AboutUsInfo, Skill, Project, ContactInfo, Video

logger = logging.getLogger(__name__) 

def home_view(request):

    team_members = TeamMember.objects.all().order_by('order')
    portfolio_categories = PortfolioCategory.objects.prefetch_related('pages').all().order_by('order')
    skills = Skill.objects.all().order_by('-level', 'name')
    projects = Project.objects.all().order_by('-completion_date')

    contact_info = ContactInfo.objects.all().last()
    videos = Video.objects.all().order_by('title')
    about_info = AboutUsInfo.objects.first() 

    # --- منطق فرم تماس ---
    if request.method == 'POST':
        logger.info("درخواست POST برای فرم تماس در home_view دریافت شد.")
        form = ContactForm(request.POST) 
        if form.is_valid():
            logger.info("فرم معتبر است. پیام در حال ذخیره در پایگاه داده.")
            try:
                form.save()
                messages.success(request, 'پیام شما با موفقیت ارسال شد!')
                logger.info("پیام با موفقیت ذخیره شد.")
                
                return redirect(reverse('home_app:home'))
            except Exception as e:
                logger.error(f"خطا در ذخیره پیام: {e}")
                messages.error(request, 'مشکلی در ذخیره پیام شما پیش آمد. لطفا دوباره تلاش کنید.')
        else:
            logger.warning("فرم معتبر نیست. خطاها: %s", form.errors) 
            messages.error(request, 'لطفاً خطاهای فرم را بررسی کنید. (مثال: ایمیل نامعتبر، فیلدهای خالی)')
    else:
        logger.info("درخواست GET دریافت شد. فرم تماس خالی مقداردهی اولیه می‌شود.")
        form = ContactForm() 
 

    context = {
        'team_members': team_members,
        'portfolio_categories': portfolio_categories,
        'skills': skills,
        'projects': projects,
        'contact_info': contact_info,
        'videos': videos,
        'form': form, 
        'about_info': about_info,
    }
    return render(request, 'Home_app/index.html', context)


def about_view(request):

    about_info = AboutUsInfo.objects.first()
    context = {
        'about_info': about_info,
    }
    return render(request, 'Home_app/aboutus.html', context)

def services_view(request):

    context = {}
    return render(request, 'Home_app/services.html', context)

def portfolio_detail_view(request, pk):

    page = get_object_or_404(PortfolioPage, pk=pk)
    context = {
        'page': page
    }
    return render(request, 'Home_app/portfolio_detail.html', context)

def skills_view(request):

    skills = Skill.objects.all().order_by('-level', 'name')
    context = {
        'skills': skills,
    }
    return render(request, 'Home_app/skills.html', context)
