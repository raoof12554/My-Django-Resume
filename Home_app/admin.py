# Home_app/admin.py
from django.contrib import admin
from .models import Project, Skill, ContactInfo, Video, PortfolioCategory, PortfolioPage, AboutUsInfo

admin.site.register(Project)
admin.site.register(Skill)
admin.site.register(ContactInfo)
admin.site.register(Video)
admin.site.register(PortfolioCategory)
admin.site.register(PortfolioPage)
admin.site.register(AboutUsInfo)