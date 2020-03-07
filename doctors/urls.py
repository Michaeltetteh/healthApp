from django.urls import path
from .views import HomePage

app_name = 'doctors'

urlpatterns = [
    path('home/',HomePage,name='doctor-homepage'),
]


