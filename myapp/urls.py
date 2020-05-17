from django.urls import path
from . import views
from django.urls import include
from django.contrib import admin

urlpatterns = [

    path('', views.homeView, name = 'home'),
    path('new_search', views.newSearch, name = 'newSearch'),
    path('detailed_search', views.detailedSearchView, name='detailedSearchView'),
    path('accounts/', include('django.contrib.auth.urls')),
    path("register", views.register, name="register"),
    path('subscribe', views.notificationView, name ='send'),
    path('subscribed', views.subscribed, name = 'subscribed'),
]