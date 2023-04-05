from django.urls import path

from .views import index, user_login, logout_user, register, user_home_page, company_register, company_login, \
    company_home_page, admin_login, all_companies, delete_company, change_status, accepted_company, rejected_company, \
    pending_company

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

    # admin
    path("admin_login/", admin_login, name="admin_login"),
    path("all_companies/", all_companies, name="all_companies"),
    path("delete_company/<int:myid>/", delete_company, name="delete_company"),
    path("change_status/<int:myid>/", change_status, name="change_status"),
    path("accepted_companies/", accepted_company, name="accepted_companies"),
    path("rejected_company/", rejected_company, name="rejected_company"),
    path("pending_companies/", pending_company, name="pending_companies"),

]
