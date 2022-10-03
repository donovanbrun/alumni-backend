from rest_framework import viewsets, generics, permissions, status

from rest_framework.response import Response
from .serializers import StudentSerializer, CompanySerializer, LinkSerializer, FileUploadSerializer
from .models import Student, Company, Link

import pandas as pd


class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all().order_by('first_name')
    serializer_class = StudentSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all().order_by('name')
    serializer_class = CompanySerializer


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class StudentsWithCompaniesView(generics.ListCreateAPIView):

    def get(self, request, format=None):
        students = Student.objects.all()
        links = Link.objects.all()
        response = []
        for student in students:
            linksForStudent = links.filter(student=student)
            response.append({
                "student" : StudentSerializer(student).data,
                "host_company": CompanySerializer(linksForStudent.first().company).data,
                "host_company_job": linksForStudent.first().job_title,
                "actual_company": CompanySerializer(linksForStudent.last().company).data,
                "actual_company_job": linksForStudent.last().job_title,
            })
        return Response(response)


class StudentsWithCompaniesByPromotionView(generics.ListCreateAPIView):

    def get(self, request, promotion, format=None):
        students = Student.objects.all().filter(promotion=promotion)
        links = Link.objects.all()
        response = []
        for student in students:
            linksForStudent = links.filter(student=student)
            response.append({
                "student": StudentSerializer(student).data,
                "host_company": CompanySerializer(linksForStudent.first().company).data,
                "host_company_job": linksForStudent.first().job_title,
                "actual_company": CompanySerializer(linksForStudent.last().company).data,
                "actual_company_job": linksForStudent.last().job_title,
            })
        return Response(response)


class StudentGenderSpecificPromotion(generics.CreateAPIView):

    def get(self, request, promotion, format=None):
        querysetPromotion = Student.objects.filter(promotion = promotion)
        querysetGirls = querysetPromotion.filter(gender="FEMME").count()
        querysetMen = querysetPromotion.filter(gender="HOMME").count()
        return Response({
            "PROMOTION" : promotion,
            "FEMME" : querysetGirls,
            "HOMME" : querysetMen,
        })


class StudentGender(generics.ListCreateAPIView):

    def get(self, request, format=None):
        students = Student.objects.all().order_by('promotion')
        response = {}
        for student in students :
            if response.get(student.promotion) is not None :
                if student.gender == "FEMME" :
                    response[student.promotion]["FEMME"] = response[student.promotion]["FEMME"]+1
                else :
                    response[student.promotion]["HOMME"] = response[student.promotion]["HOMME"]+1
            else :
                response[student.promotion] = {
                    "PROMOTION" : student.promotion,
                    "FEMME" : 0,
                    "HOMME" : 0,
                }
                if student.gender == "FEMME" :
                    response[student.promotion]["FEMME"] = response[student.promotion]["FEMME"]+1
                else :
                    response[student.promotion]["HOMME"] = response[student.promotion]["HOMME"]+1
        keys = response.keys()
        resp = []
        for key in keys :
            resp.append(response.get(key))

        return Response(resp)


class NumberStudentCompanyPromotion(generics.CreateAPIView) :

    def get(self, request, promotion, format=None) :
        response = {}
        variableLink = Link.objects.all().filter(is_host_company=True)
        for link in variableLink :
            if link.student.promotion == promotion :
                if response.get(link.company.name) is not None and link.is_host_company is True :
                    response[link.company.name]["NUMBER"] = response[link.company.name]["NUMBER"]+1
                else :
                    response[link.company.name] = {
                        "NAME" : link.company.name,
                        "NUMBER" : 1
                    }
        keys = response.keys()
        resp = []
        for key in keys :
            resp.append(response.get(key))
        resp.sort(key=lambda x: x.get('NUMBER'), reverse=True)
        return Response(resp)
        

class NumberStudentCompany(generics.ListCreateAPIView) :

    def get(self, request, format=None) :
        response = {}
        variableLink = Link.objects.all().filter(is_host_company=True)
        for link in variableLink :
            if response.get(link.company.name) is not None and link.is_host_company is True :
                response[link.company.name]["NUMBER"] = response[link.company.name]["NUMBER"]+1
            else :
                response[link.company.name] = {
                    "NAME" : link.company.name,
                    "NUMBER" : 1
                }
        keys = response.keys()
        resp = []
        for key in keys :
            resp.append(response.get(key))
        resp.sort(key=lambda x: x.get('NUMBER'), reverse=True)
        return Response(resp)


class AlumniSituationPromotion(generics.CreateAPIView):

    def get(self, request, promotion, format=None):
        response = {
            "PROMOTION": promotion,
            "STAYING": 0,
            "CHANGING": 0,
            "NOTWORKING": 0
        }
        studentForProm = Student.objects.all().filter(promotion=promotion)
        links = Link.objects.all()

        for student in studentForProm:
            linksOfStudent = links.filter(student=student)
            if linksOfStudent.last().company.name == "INCONNU":
                response["NOTWORKING"] += 1
            elif linksOfStudent.first().company.name + " " + linksOfStudent.first().company.city == linksOfStudent.last().company.name + " " + linksOfStudent.last().company.city:
                response["STAYING"] += 1
            else:
                response["CHANGING"] += 1
        return Response(response)


class AlumniSituation(generics.CreateAPIView):

    def get(self, request, format=None):
        response = {}
        students = Student.objects.all().filter().order_by('promotion')
        links = Link.objects.all()

        for student in students:
            if response.get(student.promotion) is not None:
                linksOfStudent = links.filter(student=student)
                if linksOfStudent.last().company.name == "INCONNU":
                    response[student.promotion]["NOTWORKING"] += 1
                elif linksOfStudent.first().company.name + " " + linksOfStudent.first().company.city == linksOfStudent.last().company.name + " " + linksOfStudent.last().company.city:
                    response[student.promotion]["STAYING"] += 1
                else:
                    response[student.promotion]["CHANGING"] += 1
            else:
                response[student.promotion] = {
                    "PROMOTION": student.promotion,
                    "STAYING": 0,
                    "CHANGING": 0,
                    "NOTWORKING": 0
                }
                linksOfStudent = links.filter(student=student)
                if linksOfStudent.last().company.name == "INCONNU":
                    response[student.promotion]["NOTWORKING"] += 1
                elif linksOfStudent.first().company.name + " " + linksOfStudent.first().company.city == linksOfStudent.last().company.name + " " + linksOfStudent.last().company.city:
                    response[student.promotion]["STAYING"] += 1
                else:
                    response[student.promotion]["CHANGING"] += 1

        keys = response.keys()
        resp = []
        for key in keys:
            resp.append(response.get(key))

        return Response(resp)


class ListPromotions(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        promotions = Student.objects.values('promotion').distinct()
        return Response(promotions)

    def delete(self, request, format=None, promotion=None):
        Student.objects.filter(promotion=promotion).delete()
        return Response({
            "message": "la promotion a bien été supprimée"
        })


class StudentByPromotion(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        promotion = request.query_params.get("promotion")
        if promotion.isnumeric():
            queryset = Student.objects.all().filter(promotion=promotion)
            serializer = StudentSerializer(queryset, many=True)
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            "message": "Il faut renseigner le paramètre promotion"
        })


class AddPromoView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        file = serializer.validated_data['file']
        reader = pd.read_csv(file, sep=",", header=0, names=["Prenom", "Nom de famille", "Promotion", "Email", "Genre", "Diplome", "Entreprise d'accueil", "Ville entreprise d'accueil", "Profession d'accueil", "Entreprise", "Ville entreprise", "Profession", "Linkedin"])

        for _, row in reader.iterrows():
            newStudent = Student(
                first_name=row["Prenom"],
                last_name=row["Nom de famille"],
                gender=row["Genre"],
                email=row["Email"],
                promotion=row["Promotion"],
                degree=row["Diplome"],
                linkedin=row["Linkedin"]
            )
            newStudent.save()

            # Creation of link for host company
            possibleCompany = Company.objects.all().filter(name=str(row["Entreprise d'accueil"]).upper(), city=str(row["Ville entreprise d'accueil"]).upper())
            isExist = possibleCompany.exists()
            company = None

            if isExist:
                company = possibleCompany.first()
            else:
                newCompany = Company(
                    name=str(row["Entreprise d'accueil"]).upper(),
                    city=str(row["Ville entreprise d'accueil"]).upper(),
                    is_partner=False
                )
                newCompany.save()
                company = newCompany

            newLink = Link(
                student=newStudent,
                company=company,
                job_title=row["Profession d'accueil"],
                is_host_company=True
            )
            newLink.save()

            # Creation of link for actual company
            possibleCompany = Company.objects.all().filter(name=str(row["Entreprise"]).upper(), city=str(row["Ville entreprise"]).upper())
            isExist = possibleCompany.exists()
            company = None

            if isExist:
                company = possibleCompany.first()
            else:
                newCompany = Company(
                    name=str(row["Entreprise"]).upper(),
                    city=str(row["Ville entreprise"]).upper(),
                    is_partner=False
                )
                newCompany.save()
                company = newCompany

            newLink = Link(
                student=newStudent,
                company=company,
                job_title=row["Profession"],
                is_host_company=False
            )
            newLink.save()

        return Response({"status": "success"}, status.HTTP_201_CREATED)


class AddStudentView(generics.CreateAPIView):

    def post(self, request, *args, **kwargs):
        data = request.data
        newStudent = Student(
            first_name=data["Prenom"],
            last_name=data["Nom de famille"],
            gender=data["Genre"],
            email=data["Email"],
            promotion=data["Promotion"],
            degree=data["Diplome"],
            linkedin=data["Linkedin"]
        )

        newStudent.save()

        possibleCompany = Company.objects.all().filter(name=str(data["Entreprise d'accueil"]).upper(),
                                                       city=str(data["Ville entreprise d'accueil"]).upper())
        isExist = possibleCompany.exists()
        company = None

        if isExist:
            company = possibleCompany.first()
        else:
            newCompany = Company(
                name=str(data["Entreprise d'accueil"]).upper(),
                city=str(data["Ville entreprise d'accueil"]).upper(),
                is_partner=False
            )
            newCompany.save()
            company = newCompany

        newLink = Link(
            student=newStudent,
            company=company,
            job_title=data["Profession d'accueil"],
            is_host_company=True
        )
        newLink.save()

        # Creation of link for actual company
        possibleCompany = Company.objects.all().filter(name=str(data["Entreprise"]).upper(),
                                                       city=str(data["Ville entreprise"]).upper())
        isExist = possibleCompany.exists()
        company = None

        if isExist:
            company = possibleCompany.first()
        else:
            newCompany = Company(
                name=str(data["Entreprise"]).upper(),
                city=str(data["Ville entreprise"]).upper(),
                is_partner=False
            )
            newCompany.save()
            company = newCompany

        newLink = Link(
            student=newStudent,
            company=company,
            job_title=data["Profession"],
            is_host_company=False
        )
        newLink.save()

        return Response({"status": "success"}, status.HTTP_201_CREATED)
