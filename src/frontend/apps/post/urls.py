from django.urls import path

from . import views

urlpatterns = [
    path('', views.listNews, name='listNews'),
    path('post/<int:_id>/', views.getNews, name='getNews'),
    path('post/<int:_id>/delete/', views.deleteNews, name='deleteNews'),
]
