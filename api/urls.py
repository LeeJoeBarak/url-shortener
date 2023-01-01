
from django.urls import path
from .views import home, createShortURL, redirect

urlpatterns = [
    path('', home),
    path('create', createShortURL, name='create'),
    path('<str:short_url>', redirect, name='redirect')
]