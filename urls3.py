04.18 12:00 PM


from django.urls import path,include
from . import views

urlpatterns = [
    path("", views.Index, name="index"),
    path("register", views.register, name="register"),
    path("registration", views.Registration, name="registration"),
    path("home", views.home, name="home"),
    path("login", views.Loginview, name="login"),
    path("votingpage/<int:pk>", views.Voting, name="votingpage"),
    path("showques", views.show, name="show"),
    path("logout", views.signout, name="logout"),
    path("successfully", views.successfully, name="successfully"),
    path("already", views.already, name="already")
]
