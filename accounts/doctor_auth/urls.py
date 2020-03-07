from django.urls import path
from .views import LoginView,SignUpView,LogoutView


urlpatterns = [
    path('',LoginView.as_view(),name='doctor_login'),
    path('doctor/register/',SignUpView.as_view(),name='doctor_register'),
    path('doctor/logout/',LogoutView.as_view(),name='doctor-logout'),
]





