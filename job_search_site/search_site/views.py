from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Applicant, Job, Company, Application, User


def index(request):
    return render(request, "index.html")




def user_login(request):
    if request.user.is_authenticated and (not request.user.is_superuser or not request.user.is_staff):
        return redirect("index")

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

        return redirect("user_home_page")

    return render(request, "register.html")


def logout_user(request):
    logout(request)
    return redirect("index")


def user_home_page(request):
    if not request.user.is_authenticated:
        return redirect('user_login')

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
    jobs = Job.objects.all().order_by("-start_date")
    applicant = Applicant.objects.get(user=request.user)
    apply = Application.objects.filter(applicant=applicant)
    data = []
    for i in apply:
        data.append(i)

    return render(request, "all_jobs.html", {"jobs": jobs, "data": data})


def job_details(request, job_id):
    job = Job.objects.filter(id=job_id)

    return render(request, "job_details.html", {"job": job})


def company_register(request):
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


def job_list(request):
    if not request.user.is_authenticated:
        return redirect("company_login")
    try:
        companies = Company.objects.get(user=request.user)

        jobs = Job.objects.filter(company=companies)
    except:
        return render(request, "job_list.html")

    return render(request, "job_list.html", {'jobs': jobs})


def add_job(request):
    if not request.user.is_authenticated:
        return redirect("company_login")

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


def admin_login(request):
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
    if not request.user.is_authenticated:
        return redirect("admin_login")

    companies = Company.objects.all()

    return render(request, "all_companies.html", {"companies": companies})


def delete_company(request, myid):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    company = User.objects.filter(id=myid)
    company.delete()

    return redirect("all_companies")


def change_status(request, myid):
    if not request.user.is_authenticated:
        return redirect("admin_login")

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

    company = Company.objects.filter(status="Accepted")

    return render(request, "accepted_companies.html", {'companies': company})


def rejected_company(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    company = Company.objects.filter(status="Rejected")

    return render(request, "rejected_companies.html", {'companies': company})


def pending_company(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    company = Company.objects.filter(status="pending")

    return render(request, "pending_companies.html", {'companies': company})


def all_applicant(request):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    applicants = Applicant.objects.all()

    return render(request, "all_applicant.html", {"applicants": applicants})


def delete_applicant(request, myid):
    if not request.user.is_authenticated:
        return redirect("admin_login")

    applicant = User.objects.filter(id=myid)
    applicant.delete()

    return redirect("all_applicant")
