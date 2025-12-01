# C:\Users\admin\Desktop\resume_proje_django\djangoProject\my_team\models.py

from django.db import models

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='team/', blank=True, null=True)

    facebook_url = models.URLField(max_length=200, blank=True, null=True)
    instagram_url = models.URLField(max_length=200, blank=True, null=True)
    linkedin_url = models.URLField(max_length=200, blank=True, null=True)

    # <--- مطمئن شوید که این خط وجود دارد و درست است
    order = models.IntegerField(default=0) # این فیلد باید در مدل شما باشد

    def __str__(self):
        return f"{self.name} ({self.position})"

    class Meta:
        verbose_name = "Team Member"
        verbose_name_plural = "Team Members"
        ordering = ['order', 'name'] # <--- اینجا از فیلد 'order' استفاده شده است