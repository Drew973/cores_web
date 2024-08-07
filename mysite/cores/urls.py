# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 07:53:11 2024

@author: Drew.Bennett
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
]