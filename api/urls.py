# myapi/urls.py
from django.urls import include, path
from rest_framework import routers
from . import views
from .views import AddPromoView, AlumniSituation, AlumniSituationPromotion, NumberStudentCompany, \
    NumberStudentCompanyPromotion, StudentGender, StudentGenderSpecificPromotion, AddStudentView

router = routers.DefaultRouter()
router.register(r'students', views.StudentViewSet)
router.register(r'companies', views.CompanyViewSet)
router.register(r'links', views.LinkViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('studentWithCompanies/', views.StudentsWithCompaniesView.as_view(), name="studentWithCompanies"),
    path('studentWithCompaniesByPromotion/<int:promotion>', views.StudentsWithCompaniesByPromotionView.as_view(), name="studentWithCompaniesByPromotion"),
    path('promotions/', views.ListPromotions.as_view(), name="promotions"),
    path('promotions/<int:promotion>', views.ListPromotions.as_view(), name="promotions"),
    path('studentByPromotion', views.StudentByPromotion.as_view(), name="studentByPromotion"),
    path('upload/', AddPromoView.as_view(), name='add-promo'),
    path('addStudent/', AddStudentView.as_view(), name='add-student'),
    path('studentGenderPromotion/<int:promotion>', StudentGenderSpecificPromotion.as_view(), name='get-gender-promotion'),
    path('studentGender/', StudentGender.as_view(), name='get-genders'),
    path('companyNumber/', NumberStudentCompany.as_view(), name='get-companyNumber'),
    path('companyNumberPromotion/<int:promotion>', NumberStudentCompanyPromotion.as_view(), name='get-companyNumberYear'),
    path('alumniSituationPromotion/<int:promotion>', AlumniSituationPromotion.as_view(), name='get-situation-promotion'),
    path('alumniSituation/', AlumniSituation.as_view(), name='get-situation'),
]
