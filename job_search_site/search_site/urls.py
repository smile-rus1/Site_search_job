from django.urls import path

from .views import index, user_login, logout_user, register


urlpatterns = [
    path("", index, name='index'),
    # user
    path("user_login/", user_login, name="user_login"),
    path("logout/", logout_user, name="logout_user"),
    path("register/", register, name="register"),

]
