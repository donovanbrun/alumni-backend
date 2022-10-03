# Create your models here.
from django.db import models


class Student(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    promotion = models.IntegerField()
    email = models.EmailField()
    gender = models.CharField(max_length=100)
    degree = models.CharField(max_length=200)
    linkedin = models.URLField()

    def __str__(self):
        return self.first_name + " " + self.last_name


class Company(models.Model):
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    is_partner = models.BooleanField()

    def __str__(self):
        return self.name


class Link(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    job_title = models.CharField(max_length=200)
    is_host_company = models.BooleanField()

    def __str__(self):
        return self.student.__str__() + " " + self.company.__str__()
