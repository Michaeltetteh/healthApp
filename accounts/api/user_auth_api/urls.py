from django.contrib import admin
from django.urls import path,include,re_path

from . import views



urlpatterns = [

	path('',views.indexPage,name="indexPage"),
    path('signup/',views.doctorRegister, name="doc_reg"),
    
    #api/doctor/login
    path('login/',views.UserLoginAPIView.as_view(),name='login'),
    #api/doctor/register
    path('register/',views.DoctorRegistrationAPIView.as_view(),name='register'),

    
    re_path(r'^verify/(?P<verification_key>.+)/$',views.UserEmailVerificationAPIView.as_view(),name='email_verify'),

    # path('password_reset/',views.PasswordResetAPIView.as_view(),name='password_change'),

    # re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),

    path('user-profile/',views.UserProfileAPIView.as_view(),name='user_profile'),


]
