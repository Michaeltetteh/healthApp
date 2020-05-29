from django.urls import path
from .views import HomePage

app_name = 'doctors'

urlpatterns = [
    path('home/',HomePage,kwargs={},name='doctor-homepage'),
]


