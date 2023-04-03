from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import Applicant, Job, Company, Application


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
                    return redirect("user_homepage")
            else:
                thank = True
                return render(request, "user_login.html", {"thank": thank})

    return render(request, "user_login.html")


def register(request):

    return render(request, "register.html")

def logout_user(request):
    logout(request)
    return redirect("index")
