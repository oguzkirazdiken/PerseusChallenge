from django.urls import path, re_path
from api import views


urlpatterns = [
    path('api/userCreate/', views.user_create, name='user_create'),
    path('api/courseCreate/', views.course_create, name='course_create'),
    path('api/certificateCreate/', views.certificate_create, name='certificate_create'),
]