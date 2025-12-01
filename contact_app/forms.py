# C:\Users\admin\Desktop\resume_proje_django\djangoProject\contact_app\forms.py

from django import forms
from .models import Message

class ContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['fname', 'email', 'sub', 'body']
        labels = {
            'fname': 'نام و نام خانوادگی',
            'email': 'ایمیل',
            'sub': 'موضوع',
            'body': 'توضیحات', # می‌توانید این را بر اساس نیاز خود تغییر دهید
        }
        # widgets = { ... } # <--- این بخش را کاملاً حذف کنید یا کامنت کنید