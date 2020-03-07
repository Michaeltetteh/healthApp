from django.urls import path,include

app_name = 'accounts'

urlpatterns = [
    path('',include('accounts.doctor_auth.urls')),
    path('p/',include('accounts.patient_auth.urls')),
]





