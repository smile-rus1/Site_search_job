from django.urls import path

from .views import index, user_login, logout_user, register, user_home_page, company_register, company_login, \
    company_home_page

urlpatterns = [
    path("", index, name='index'),
    # user
    path("user_login/", user_login, name="user_login"),
    path("logout/", logout_user, name="logout_user"),
    path("register/", register, name="register"),
    path("user_home_page/", user_home_page, name="user_home_page"),

    # company
    path("company_login/", company_login, name="company_login"),
    path("company_register/", company_register, name="company_register"),
    path("company_home_page/", company_home_page, name="company_home_page"),
]
