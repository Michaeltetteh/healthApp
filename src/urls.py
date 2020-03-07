from django.contrib import admin
from django.urls import path,include
from chart import urls
from patients import endpoints
from . import views


# TODO: change django admin title
admin.site.site_header = "HealthApi"
admin.site.site_title = "HealthApi Admin Portal"
admin.site.index_title = "HealthApi"

urlpatterns = [
    # path('',include('accounts.api.user_auth_api.urls')),
    path('',include('accounts.urls')),
    path('patient/',include('patients.urls')),
    path('doctor/',include('doctors.urls')),
    path('chart/', include('chart.urls')),
    path('admin/', admin.site.urls),

    path(r'api/pulse/<str:device>/<int:datapoints>', endpoints.pusle_chart_by_device, name="api_pulse2"),

    
]





