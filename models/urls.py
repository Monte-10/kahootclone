from django.urls import path
from . import views
from django.conf.urls import url
from django.urls import reverse

urlpatterns = [
    path('', views.home, name='home'),
]