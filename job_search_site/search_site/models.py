from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User


phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")


class Applicant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=16, validators=[phoneNumberRegex], unique=True)
    image = models.ImageField(upload_to="")
    gender = models.CharField(max_length=10)
    type = models.CharField(max_length=15)

    def __str__(self):
        return self.user.first_name

    class Meta:
        verbose_name_plural = "Кандитаты"


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=16, validators=[phoneNumberRegex], unique=True)
    image = models.ImageField(upload_to="")
    gender = models.CharField(max_length=10)
    type = models.CharField(max_length=15)
    status = models.CharField(max_length=20)
    company_name = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural = "Компании"


class Job(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    title = models.CharField(max_length=200)
    salary = models.FloatField()
    image = models.ImageField(upload_to="")
    description = models.CharField(max_length=400)
    experience = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    skills = models.CharField(max_length=200)
    creation_date = models.DateField()

    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Работа"
        ordering = ["start_date"]


class Application(models.Model):
    company = models.CharField(max_length=200, default="")
    resume = models.ImageField(upload_to="")
    apply_date = models.DateField()

    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    job = models.ForeignKey(Job, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.applicant)

    class Meta:
        verbose_name_plural = "Отправка резюме"


class News(models.Model):
    title = models.CharField(max_length=50, null=False)
    content = models.CharField(max_length=500, null=False)
    date_add = models.DateField(auto_now_add=True, null=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name_plural = "Новости"
        ordering = ["-date_add"]
