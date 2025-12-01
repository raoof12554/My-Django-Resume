from django.shortcuts import render, redirect 
from .models import Project, Skill, ContactInfo, Video, AboutUsInfo
from contact_app.models import Message 




def home_view(request):
    if request.method == "POST": 
        fname = request.POST.get('fname')
        email = request.POST.get('email')
        sub = request.POST.get('subject') 
        body = request.POST.get('body')

        if fname and email and sub and body: # یک اعتبارسنجی اولیه
            Message.objects.create(fname=fname, email=email, sub=sub, body=body)
            return redirect('home_view_name') 
        else:

            pass 

    projects = Project.objects.all()
    skills = Skill.objects.all()
    contact_info = ContactInfo.objects.first()
    about_info = AboutUsInfo.objects.first()
    videos = Video.objects.all()
    
    context = {
        'projects': projects,
        'skills': skills,
        'contact_info': contact_info,
        'videos': videos,
        'about_info': about_info, 
    }
    return render(request, 'Home_app/index.html', context)