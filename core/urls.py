from django.contrib import admin
from django.urls import path, include

from core.views import homepage

app_name = 'core'

urlpatterns = [
    path('', homepage, name='home-page'),
]
