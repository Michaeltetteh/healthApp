from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from rest_framework import generics, permissions, status, views
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

from accounts.models import UserProfile
from . import serializer
from django.http import HttpResponse

from django.shortcuts import render,redirect
from patients.views import index

from rest_framework.renderers import TemplateHTMLRenderer

User = get_user_model()




# user signin page
def indexPage(request):
    return render(request, "doctor/login.html") 

def doctorRegister(request):
    return render(request, "doctor/register.html")



class DoctorRegistrationAPIView(generics.CreateAPIView):
    """
    Endpoint for doctor registration.

    """
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "doctor/register.html"

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializer.DoctorRegistrationSerializer
    queryset = User.objects.all()
    


class UserEmailVerificationAPIView(views.APIView):
    """
    Endpoint for verifying email address.

    """

    permission_classes = (permissions.AllowAny, )

    def get(self, request, verification_key):
        activated_user = self.activate(verification_key)
        if activated_user:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def activate(self, verification_key):
        return UserProfile.objects.activate_user(verification_key)




class UserLoginAPIView(views.APIView):
    """
    Endpoint for user login. Returns authentication token on success.

    """
    permission_classes = (permissions.AllowAny, )
    serializer_class = serializer.UserLoginSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "doctor/login.html"

    def get_user_profile(self, username):
        try:
            user_profile = UserProfile.objects.get(user__username=username)
        except:
            return None
        return user_profile
    
    def post(self, request):
        # print(request.data)
        # print()
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            # return Response(serializer.data, status=status.HTTP_200_OK)
            # print(serializer.data) #token response
            if status.HTTP_200_OK:
                return redirect('index')  #redirect to doctor's home page
                
            # user_profile = self.get_user_profile(request.data.get('username'))
            # if user_profile:
            #     if status.HTTP_200_OK:
            #         return redirect('index')  #redirect to doctor's home page
            #      # To be made asynchronous in production
            # # return Response(status=status.HTTP_200_OK)

                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetAPIView(views.APIView):
    """
    Endpoint to send email to user with password reset link.

    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializer.PasswordResetSerializer

    def post(self, request):
        user_profile = self.get_user_profile(request.data.get('email'))
        if user_profile:
            user_profile.send_password_reset_email(
                site=get_current_site(request)
            )  # To be made asynchronous in production
            return Response(status=status.HTTP_200_OK)

        # Forcing Http status to 200 even if failure to support user privacy.
        # Will show message at frontend like "If the email is valid, you must have received password reset email"
        return Response(status=status.HTTP_200_OK)

    def get_user_profile(self, email):
        try:
            user_profile = UserProfile.objects.get(user__email=email)
        except:
            return None
        return user_profile


class PasswordResetConfirmView(views.APIView):
    """
    Endpoint to change user password.

    """

    permission_classes = (permissions.AllowAny, )
    serializer_class = serializer.PasswordResetConfirmSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(
            data=request.data,
            context={
                'uidb64': kwargs['uidb64'],
                'token': kwargs['token']
            })

        if serializer.is_valid(raise_exception=True):
            new_password = serializer.validated_data.get('new_password')
            user = serializer.user
            user.set_password(new_password)
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileAPIView(generics.RetrieveAPIView):
    """
    Endpoint to retrieve user profile.

    """

    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = (TokenAuthentication, )
    serializer_class = serializer.UserProfileSerializer

    def get_object(self):
        return self.request.user.userprofile
