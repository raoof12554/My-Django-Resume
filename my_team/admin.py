# C:\Users\admin\Desktop\resume_proje_django\djangoProject\my_team\admin.py

from django.contrib import admin
from .models import TeamMember # <-- Changed 'coursera' to 'TeamMember'

# Register your model with the admin site
# Make sure to create an admin class for your model if you want to customize its display
@admin.register(TeamMember) # <-- Register TeamMember
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'position', 'facebook_url', 'instagram_url', 'linkedin_url')
    search_fields = ('name', 'position')
    # You can add more customizations here if needed, e.g., list_filter, fields, etc.