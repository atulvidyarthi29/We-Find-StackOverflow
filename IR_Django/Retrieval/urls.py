from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('user_retrieval/', views.user_retrieval,name="user_retrieval"),
]
