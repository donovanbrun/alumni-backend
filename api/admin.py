from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Student, Company, Link

admin.site.register(Student)
admin.site.register(Company)
admin.site.register(Link)

