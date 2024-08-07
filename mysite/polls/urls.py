# -*- coding: utf-8 -*-
"""
Created on Fri Jul  5 14:01:48 2024

@author: Drew.Bennett
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]