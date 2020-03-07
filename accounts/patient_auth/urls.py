from django.urls import path
from .views import LoginView,SignUpView,LogoutView


urlpatterns = [
    path('',LoginView.as_view(),name='patient_login'),
    path('register/',SignUpView.as_view(),name='patient_register'),
    path('logout/',LogoutView.as_view(),name='patient-logout'),
]
