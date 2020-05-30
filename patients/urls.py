from . import endpoints
from rest_framework import routers
from django.urls import path,include
from . import viewsets,views

router = routers.DefaultRouter()
router.register(r'vitals', viewsets.VitalsViewSet)

app_name = 'patients'

urlpatterns = [
    path(r'api/', include(router.urls)),
    path(r'api/device/<str:device>',endpoints.str_test, name='str_test'),
    path(r'api/pulse/<str:device>', endpoints.last_pulse, name='api_pulse'),
    path(r'api/pulse/<str:device>/<int:datapoints>', endpoints.pusle_chart_by_device, name="api_pulse2"),

    path('home/', views.index, name='patient-homepage'),
    path('upload/vitals/', views.post_vitals, name='upload_pulse'),

]
