from django.urls import path

from .views import index, user_login, logout_user, register, user_home_page, company_register, company_login, \
    company_home_page, admin_login, all_companies, delete_company, change_status, accepted_company, rejected_company, \
    pending_company, all_applicant, delete_applicant, all_jobs, job_details, add_job, job_list, \
    all_applicants_for_company, job_apply, edit_job, news_user, news_company

urlpatterns = [
    path("", index, name='index'),
    # user
    path("user_login/", user_login, name="user_login"),
    path("logout/", logout_user, name="logout_user"),
    path("register/", register, name="register"),
    path("user_home_page/", user_home_page, name="user_home_page"),
    path("all_jobs/", all_jobs, name="all_jobs"),
    path("job_details/<int:job_id>", job_details, name="job_details"),
    path("job_apply/<int:myid>", job_apply, name="job_apply"),
    path("news_user", news_user, name="news_user"),

    # company
    path("company_login/", company_login, name="company_login"),
    path("company_register/", company_register, name="company_register"),
    path("company_home_page/", company_home_page, name="company_home_page"),
    path("add_job/", add_job, name="add_job"),
    path("edit_job/<int:id_job>", edit_job, name="edit_job"),
    path("job_list/", job_list, name="job_list"),
    path("all_applicants_for_company/", all_applicants_for_company, name="all_applicants_for_company"),
    path("news_company", news_company, name="news_company"),

    # admin
    path("admin_login/", admin_login, name="admin_login"),
    path("all_companies/", all_companies, name="all_companies"),
    path("delete_company/<int:myid>/", delete_company, name="delete_company"),
    path("change_status/<int:myid>/", change_status, name="change_status"),
    path("accepted_companies/", accepted_company, name="accepted_companies"),
    path("rejected_company/", rejected_company, name="rejected_company"),
    path("pending_companies/", pending_company, name="pending_companies"),
    path("all_applicants/", all_applicant, name="all_applicant"),
    path("delete_applicant/<int:myid>/", delete_applicant, name="delete_applicant"),
]
