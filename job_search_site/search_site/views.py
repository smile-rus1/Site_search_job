from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Applicant, Job, Company, Application, User


def index(request):
    return render(request, "index.html")


def user_login(request):
    if request.user.is_authenticated:
        return redirect("index")
    else:
        if request.method == "POST":
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)

            if user is not None:
                user1 = Applicant.objects.get(user=user)
                if user1.type == "applicant":
                    login(request, user)
                    return redirect("index")
            else:
                thank = True
                return render(request, "user_login.html", {"thank": thank})

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
        user.save()
        applicants.save()

        return render(request, "user_login.html")

    return render(request, "register.html")


def logout_user(request):
    logout(request)
    return redirect("index")
