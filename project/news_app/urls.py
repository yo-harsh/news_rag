from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('app/', views.news_app, name='news_app'),
]