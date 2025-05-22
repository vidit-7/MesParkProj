from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.baseHome, name="centBaseHome"),
    path('login/',views.baseLoginUser, name="centBaseLoginUser"),
    path('logout-confirm/',views.baseLogoutUser, name="centBaseLogoutUser"),
    path('register/',views.baseRegisterUser, name='centBaseRegisterUser'),
    path('profile/<str:pk>', views.baseProfile, name='centBaseProfile'),
    path('edit-profile/',views.baseEditProfile, name='centBaseEditProfile'),
    path('change-password/',views.changeUserPass, name='centBaseChangePass'),
]