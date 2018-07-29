# -*- coding : utf-8 -*-

from django.urls import path
from . import views

urlpatterns = [
    path('login', views.Login),
    path('attence', views.AddAttence),
    path('editPassword', views.EditPassword)
]

