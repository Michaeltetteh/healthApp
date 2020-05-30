from django.urls import path
from . import views
from patients import endpoints


urlpatterns = [
    path('', views.charts, name='jscharts'),
    path('pulse/', views.all_pulse_charts, name="all_pulse"),
    path('pulse/<str:device>', views.pulse_chart, name="pulse_chart"),
    path('temp/<str:device>', views.temp_chart, name='temp_chart'),
]
