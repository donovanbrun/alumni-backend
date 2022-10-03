from rest_framework import serializers

from .models import Student, Company, Link


class StudentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'promotion', 'email', 'gender', 'degree', 'linkedin')


class CompanySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'city', 'is_partner')


class LinkSerializer(serializers.HyperlinkedModelSerializer):
    student = StudentSerializer()
    company = CompanySerializer()

    class Meta:
        model = Link
        fields = ('student', 'company', 'start_date', 'end_date', 'job_title', 'is_host_company')


class FileUploadSerializer(serializers.Serializer):
    file = serializers.FileField()
