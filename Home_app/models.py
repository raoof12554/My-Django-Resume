# C:\Users\admin\Desktop\resume_proje_django\djangoProject\Home_app\models.py

from django.db import models
from django.urls import reverse

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team_members/')
    facebook_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    order = models.PositiveIntegerField(default=0, help_text="The display order for this team member.")

    class Meta:
        ordering = ['order']
        verbose_name = "عضو تیم"
        verbose_name_plural = "اعضای تیم"

    def __str__(self):
        return self.name

class PortfolioCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0, help_text="The display order for this category.")

    class Meta:
        ordering = ['order']
        verbose_name = "دسته بندی نمونه کار"
        verbose_name_plural = "دسته بندی های نمونه کار"

    def __str__(self):
        return self.name

class PortfolioPage(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(PortfolioCategory, on_delete=models.CASCADE, related_name='pages')
    image = models.ImageField(upload_to='portfolio/')
    order = models.PositiveIntegerField(default=0, help_text="The display order for this portfolio item.")
    description = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['order']
        verbose_name = "صفحه نمونه کار"
        verbose_name_plural = "صفحات نمونه کار"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('home_app:portfolio_detail', args=[self.pk])


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='projects/', blank=True, null=True)
    completion_date = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = "پروژه"
        verbose_name_plural = "پروژه ها"

    def __str__(self):
        return self.title

class Skill(models.Model):
    name = models.CharField(max_length=100)
    level = models.IntegerField(default=0)
    icon = models.CharField(max_length=50, blank=True, null=True, help_text="مثلاً 'fa-html5' برای آیکون فونت آسوم")

    class Meta:
        verbose_name = "مهارت"
        verbose_name_plural = "مهارت ها"

    def __str__(self):
        return self.name

class ContactInfo(models.Model):
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    instgram = models.CharField(max_length=200, blank=True, null=True)
    watsapp = models.CharField(max_length=200, blank=True, null=True)
    github = models.CharField(max_length=200, blank=True, null=True)
    

    class Meta:
        verbose_name = "اطلاعات تماس"
        verbose_name_plural = "اطلاعات تماس"

    def __str__(self):
        return "اطلاعات تماس"

class Video(models.Model):
    title = models.CharField(max_length=200)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "ویدئو"
        verbose_name_plural = "ویدئوها"

    def __str__(self):
        return self.title

class AboutUsInfo(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='about_us/', blank=True, null=True)

    class Meta:
        verbose_name = "درباره ما"
        verbose_name_plural = "درباره ما"

    def __str__(self):
        return self.title