from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from .models import Applicant, Job, Company, Application, User, News
from .check_all_users import check_applicant, check_company, check_admin


def index(request):
    return render(request, "index.html")


def user_login(request):
    if request.user.is_authenticated and (not request.user.is_superuser or not request.user.is_staff):
        return redirect("index")

    if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
        return redirect("all_companies")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        try:
            if user is not None:
                user1 = Applicant.objects.get(user=user)
                if user1.type == "applicant":
                    login(request, user)
                    return redirect("user_home_page")
            else:
                print(1)
                thank = True

                return render(request, "user_login.html", {"alert": thank})
        except:
            ...

    return render(request, "user_login.html")


def register(request):
    if request.user.is_authenticated and (not request.user.is_superuser or not request.user.is_staff):
        return redirect("index")

    if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
        return redirect("all_companies")

    if request.method == "POST":
        username = request.POST["username"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]
        number_phone = request.POST["phone"]
        email = request.POST["email"]
        gender = request.POST["gender"]
        image = request.FILES["image"]

        if password1 != password2:
            messages.error(request, "Пароли не совпадают!")
            return redirect('register')

        user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                        password=password1, email=email)
        applicants = Applicant.objects.create(user=user, phone=number_phone, image=image,
                                              type="applicant", gender=gender)
        login(request, user)
        user.save()
        applicants.save()

        return redirect("company_login")

    return render(request, "register.html")


def logout_user(request):
    logout(request)
    return redirect("index")


def news_user(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    if not check_applicant(request):
        logout(request)
        return redirect("index")

    news = News.objects.all()

    return render(request, "user_news.html", {"news": news})


def user_home_page(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

    if not check_applicant(request):
        logout(request)
        return redirect("index")

    applicant = Applicant.objects.get(user=request.user)

    if request.method == "POST":
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        gender = request.POST['gender']

        applicant.user.email = email
        applicant.user.first_name = first_name
        applicant.user.last_name = last_name
        applicant.phone = phone
        applicant.gender = gender
        applicant.save()
        applicant.user.save()

        try:
            image = request.FILES['image']
            applicant.image = image
            applicant.save()

        except:
            pass

        alert = True

        return render(request, "user_home_page.html", {'alert': alert})

    return render(request, "user_home_page.html", {'applicant': applicant})


def all_jobs(request):
    if not check_applicant(request):
        logout(request)

        return redirect("index")

    jobs = Job.objects.all().order_by("-start_date")
    applicant = Applicant.objects.get(user=request.user)
    apply = Application.objects.filter(applicant=applicant)
    data = []
    for i in apply:
        data.append(i.job.id)

    return render(request, "all_jobs.html", {"jobs": jobs, "data": data})


def job_details(request, job_id):
    if not check_applicant(request):
        logout(request)

        return redirect("index")

    job = Job.objects.get(id=job_id)

    return render(request, "job_details.html", {"job": job})


def job_apply(request, myid: int):
    if not check_applicant(request):
        logout(request)

    applicant = Applicant.objects.get(user=request.user)
    job = Job.objects.get(id=myid)
    date1 = date.today()

    if job.end_date < date1:
        closed = True

        return render(request, "job_apply.html", {"closed": closed})

    elif job.start_date > date1:
        notopen = True

        return render(request, "job_apply.html", {"notopen": notopen})

    else:
        if request.method == "POST":
            resume = request.FILES["resume"]
            Application.objects.create(job=job, company=job.company, applicant=applicant, resume=resume,
                                       apply_date=date.today())

            alert = True

            return render(request, "job_apply.html", {"alert": alert})

    return render(request, "job_apply.html", {"job": job})


def company_register(request):
    if request.user.is_authenticated and (not request.user.is_superuser or not request.user.is_staff):
        return redirect("company_home_page")

    if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
        return redirect("all_companies")

    if request.user.is_authenticated:
        return redirect("company_home_page")

    try:
        if request.method == "POST":
            username = request.POST["username"]
            first_name = request.POST["first_name"]
            last_name = request.POST["last_name"]
            password1 = request.POST["password1"]
            password2 = request.POST["password2"]
            number_phone = request.POST["phone"]
            email = request.POST["email"]
            gender = request.POST["gender"]
            image = request.FILES["image"]
            company_name = request.POST['company_name']

            if password1 != password2:
                messages.error(request, "Пароли не совпадают!")

                return redirect("company_register")

            user = User.objects.create_user(first_name=first_name, last_name=last_name, email=email, username=username,
                                            password=password1)

            company = Company.objects.create(user=user, phone=number_phone, gender=gender, image=image,
                                             company_name=company_name, type="company", status="pending")
            user.save()
            company.save()

            return redirect("company_home_page")
    except:
        messages.error(request, "Возникла ошибка в заполнеии")

    return render(request, "company_register.html")


def company_login(request):
    if request.user.is_authenticated and (not request.user.is_superuser or not request.user.is_staff):
        return redirect("company_home_page")

    if request.user.is_authenticated and (request.user.is_superuser or request.user.is_staff):
        return redirect("all_companies")

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            user1 = Company.objects.get(user=user)

            if user1.type == "company" and user1.status == "pending":
                messages.info(request, "Подождите пока администратор одобрит заявку")

                message = True
                return render(request, "company_login.html", {"message": message})

            # будет менять статус админ который будет смотреть
            if user1.type == "company" and user1.status != "pending":
                login(request, user)
                return redirect("company_home_page")
        else:
            alert = True

            return render(request, "company_login.html", {"alert": alert})

    return render(request, "company_login.html")


def company_home_page(request):
    if not request.user.is_authenticated:
        return redirect("company_login")

    if not check_company(request):
        logout(request)

        return redirect("index")

    company = Company.objects.get(user=request.user)

    if request.method == "POST":
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phone = request.POST['phone']
        gender = request.POST['gender']

        company.user.email = email
        company.user.first_name = first_name
        company.user.last_name = last_name
        company.phone = phone
        company.gender = gender
        company.save()
        company.user.save()

        try:
            image = request.FILES['image']
            company.image = image
            company.save()

        except:
            pass

        thank = True

        return render(request, "company_home_page.html", {'alert': thank})

    return render(request, "company_home_page.html", {'company': company})


def news_company(request):
    if not request.user.is_authenticated:
        return redirect("company_login")

    if not check_company(request):
        logout(request)

        return redirect("index")

    news = News.objects.all()

    return render(request, "company_news.html", {"news": news})


def all_applicants_for_company(request):
    if not request.user.is_authenticated:
        return redirect("company_login")

    if not check_company(request):
        logout(request)

        return redirect("index")

    company = Company.objects.get(user=request.user)
    application = Application.objects.filter(company=company).order_by("-apply_date")

    return render(request, "applicants_for_company.html", {'application': application})


def job_list(request):
    if not request.user.is_authenticated:
        return redirect("company_login")

    if not check_company(request):
        logout(request)

        return redirect("index")

    try:
        companies = Company.objects.get(user=request.user)

        jobs = Job.objects.filter(company=companies)
    except:
        return render(request, "job_list.html")

    return render(request, "job_list.html", {'jobs': jobs})


def add_job(request):
    if not request.user.is_authenticated:
        return redirect("company_login")

    if not check_company(request):
        logout(request)

        return redirect("index")

    try:
        if Company.objects.get(user=request.user):
            ...
    except:
        return redirect("company_login")

    if request.method == "POST":
        title = request.POST["job_title"]
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]
        experience = request.POST["experience"]
        salary = request.POST["salary"]
        skills = request.POST["skills"]
        description = request.POST["description"]
        location = request.POST["location"]

        user = request.user
        company = Company.objects.get(user=user)
        job = Job.objects.create(company=company, title=title, start_date=start_date, end_date=end_date, salary=salary,
                                 experience=experience, skills=skills, description=description, image=company.image,
                                 creation_date=date.today(), location=location)
        job.save()
        alert = True

        return render(request, "add_jobs.html", {"alert": alert})

    return render(request, "add_jobs.html")


def edit_job(request, id_job: int):
    if not request.user.is_authenticated:
        return redirect("company_login")

    if not check_company(request):
        logout(request)

        return redirect("index")

    job = Job.objects.get(id=id_job)

    if request.method == "POST":
        title = request.POST['job_title']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        salary = request.POST['salary']
        experience = request.POST['experience']
        location = request.POST['location']
        skills = request.POST['skills']
        description = request.POST['description']

        job.title = title
        job.salary = salary
        job.experience = experience
        job.location = location
        job.skills = skills
        job.description = description

        job.save()

        if start_date:
            job.start_date = start_date
            job.save()

        if end_date:
            job.end_date = end_date
            job.save()

        alert = True

        return render(request, "edit_job.html", {"alert": alert})

    return render(request, "edit_job.html", {"job": job})


def admin_login(request):
    if request.user.is_authenticated:
        return redirect("all_companies")

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        try:
            if user.is_superuser:
                login(request, user)

                return redirect("all_companies")

            else:
                alert = True

                return render(request, "admin_login.html", {"alert": alert})
        except:
            alert = True
            return render(request, "admin_login.html", {"alert": alert})

    return render(request, "admin_login.html")


def all_companies(request):
    if not check_admin(request):
        logout(request)

        return redirect("index")

    if not request.user.is_authenticated:
        return redirect("admin_login")

    companies = Company.objects.all()

    return render(request, "all_companies.html", {"companies": companies})


def delete_company(request, myid):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not check_admin(request):
        logout(request)

        return redirect("index")

    company = User.objects.filter(id=myid)
    company.delete()

    return redirect("all_companies")


def change_status(request, myid):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not check_admin(request):
        logout(request)

        return redirect("index")

    company = Company.objects.get(id=myid)

    if request.method == "POST":
        status = request.POST["status"]
        company.status = status
        company.save()
        alert = True
        return render(request, "change_status.html", {'alert': alert})

    return render(request, "change_status.html", {"company": company})


def accepted_company(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not check_admin(request):
        logout(request)

        return redirect("index")

    company = Company.objects.filter(status="Accepted")

    return render(request, "accepted_companies.html", {'companies': company})


def rejected_company(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not check_admin(request):
        logout(request)

        return redirect("index")

    company = Company.objects.filter(status="Rejected")

    return render(request, "rejected_companies.html", {'companies': company})


def pending_company(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not check_admin(request):
        logout(request)

        return redirect("index")

    company = Company.objects.filter(status="pending")

    return render(request, "pending_companies.html", {'companies': company})


def all_applicant(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not check_admin(request):
        logout(request)

        return redirect("index")

    applicants = Applicant.objects.all()

    return render(request, "all_applicant.html", {"applicants": applicants})


def delete_applicant(request, myid):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not check_admin(request):
        logout(request)

        return redirect("index")

    applicant = User.objects.filter(id=myid)
    applicant.delete()

    return redirect("all_applicant")


def admin_news(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not check_admin(request):
        logout(request)

        return redirect("index")

    news = News.objects.all()

    return render(request, "admin_news.html", {"news": news})


def add_news(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not check_admin(request):
        logout(request)

        return redirect("index")

    try:
        if request.method == "POST":
            title = request.POST["title"]
            content = request.POST["content"]

            news = News.objects.create(title=title, content=content, user_id=request.user.id)
            news.save()

            messages.success(request, "Статья добавлена!")
            return redirect("admin_news")
    except:
        messages.error(request, "Возникла ошибка в заполнении")

    return render(request, "add_news.html")


def delete_news(request, id_news):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not check_admin(request):
        logout(request)

        return redirect("index")

    news = News.objects.filter(id=id_news)
    news.delete()

    return redirect("admin_news")


def update_news(request, id_news: int):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    if not check_admin(request):
        logout(request)

        return redirect("index")

    news = News.objects.get(id=id_news)

    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]

        news.title = title
        news.content = content

        news.save()

        return redirect("admin_news")

    return render(request, "update_news.html", {"news": news})
