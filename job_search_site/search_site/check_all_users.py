from django.shortcuts import redirect

from .models import Applicant, Company


def check_applicant(request):
    if request.user.is_authenticated:
        try:
            check_appl = Applicant.objects.get(user=request.user)

            return True

        except:
            return False


def check_company(request):
    if request.user.is_authenticated:
        try:
            check_cmp = Company.objects.get(user=request.user)

            return True

        except:
            return False


def check_admin(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return True
