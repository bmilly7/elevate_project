from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),       # Homepage
    path('analytics/', views.analytics, name='analytics'),
    path('goals/', views.goals, name='goals'),
]