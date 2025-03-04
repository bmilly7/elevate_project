from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),
    path('dashboard/', views.dashboard, name='dashboard'),       # Homepage
    path('analytics/', views.analytics, name='analytics'),
    path('goals/', views.goals, name='goals'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile, name='profile'),
]