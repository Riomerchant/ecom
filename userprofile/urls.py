from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf import settings

# app_name='store'

urlpatterns = [
    path('',views.profile,name='profile'),
    path('profile/update/',views.update_profile,name='update-pro'),
    path('add-address/',views.add_address,name="add-address")
]