from django.shortcuts import render

# Create your views here.

def home_page(request):
    return render(request, "home.html")

def news_app(request):
    return render(request, 'index.html')