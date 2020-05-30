from django.urls import path
from .views import login_api,signup_api,dashboard_api#,logout_api LoginView,SignUpView,LogoutView,


urlpatterns = [
    # path('',LoginView.as_view(),name='patient_login'),
    # path('register/',SignUpView.as_view(),name='patient_register'),
    # path('logout/',LogoutView.as_view(),name='patient-logout'),

    #patient api
    path('api/v1/login/',login_api,name='patient-login-api'),
    path('api/v1/signup/',signup_api,name='patient-signup-api'),
    path('api/v1/dashboard/<str:device>',dashboard_api,name="dashboard"),
    # path('signout/',logout_api.as_view(),name='patient-logout-api'),
]
