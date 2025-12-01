# contact_app/admin.py

from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('fname', 'email', 'sub', 'created_at')
    search_fields = ('fname', 'email', 'sub', 'body')
    list_filter = ('created_at',)
    readonly_fields = ('created_at',)