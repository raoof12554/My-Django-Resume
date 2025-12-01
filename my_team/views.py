# C:\Users\admin\Desktop\resume_proje_django\djangoProject\my_team\views.py

from django.shortcuts import render
from .models import TeamMember # ایمپورت مدل TeamMember

def team_list_view(request):
    """
    ویو برای نمایش لیست کامل اعضای تیم در یک صفحه جداگانه.
    """
    team_members = TeamMember.objects.all().order_by('order')
    context = {
        'team_members': team_members
    }
    # فرض می‌کنیم یک قالب به نام team_list.html در پوشه templates/my_team/ دارید
    return render(request, 'my_team/team_list.html', context)