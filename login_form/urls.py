from django.contrib import admin
# from django.contrib.auth.views import LogoutView
from django.urls import path, include
from .import views
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('logout/', views.signout, name='logout'),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
]