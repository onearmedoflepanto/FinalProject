from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login),
    path("logout/", views.logout),
    path("sign_up/", views.sign_up),
    path("delete/", views.delete),
    path("mypage/", views.mypage),
    path("follow/<int:pk>/", views.follow),
    path("google/callback/", views.google_login),
]
