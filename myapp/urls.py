from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [

    path('', views.homeView, name = 'home'),
    path('new_search', views.newSearch, name = 'newSearch'),
    path('detailed_search', views.detailedSearchView, name='detailedSearchView'),
]