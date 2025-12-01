# contact_app/models.py

from django.db import models

class Message(models.Model):
    fname = models.CharField(max_length=50, verbose_name="نام و نام خانوادگی")
    email = models.EmailField(verbose_name="ایمیل")
    sub = models.CharField(max_length=100, verbose_name="موضوع")
    body = models.TextField(verbose_name="متن پیام")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ارسال")

    class Meta:
        verbose_name = "پیام تماس"
        verbose_name_plural = "پیام‌های تماس"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.fname} - {self.email} ({self.sub})"