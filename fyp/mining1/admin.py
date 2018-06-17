from django.contrib import admin

# Register your models here.

# from .models import Applicants, Applicants2016, Applicants2014
from .models import Applicants, Applicants2016

admin.site.register(Applicants)
admin.site.register(Applicants2016)
# admin.site.register(Applicants2014)