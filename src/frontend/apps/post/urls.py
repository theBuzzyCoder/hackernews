from django.urls import path

from . import views

urlpatterns = [
    path('', views.listNews, name='listNews'),
    path('<int:_id>/', views.getNews, name='getNews'),
]
