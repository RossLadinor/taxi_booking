from django.urls import path
from .views import register, login, profile, logout_view

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('profile/', profile, name='profile'),
    path('logout/', logout_view, name='logout'),
]
