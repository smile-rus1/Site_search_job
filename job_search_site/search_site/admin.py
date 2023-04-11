from django.contrib import admin
from .models import Applicant, Job, Company, Application, News


admin.site.register(Applicant)
admin.site.register(Company)
admin.site.register(Job)
admin.site.register(Application)
admin.site.register(News)
