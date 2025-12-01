# djangoProject/conect_app/views.py

from django.shortcuts import render

def conect_app_view(request):


    context = {
        'page_title': 'درباره ما / ارتباط با ما',
        'content_message': 'این محتوای اصلی Conect App است.',
        
    }
    return render(request, 'conect_app/conect_app.html', context)