from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('app/', views.news_app, name='news_app'),
    path('upload_data/', views.upload_news_data, name='upload_news_data'),
    path('chat_with_bot/', views.chat_with_bot, name='chat_with_bot'),
]