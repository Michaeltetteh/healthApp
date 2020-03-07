from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.base import View

from .forms import UserForm,ProfileForm,PatientForm

# class Index(TemplateView):
#     template_name = 'patient/index.html'

#     def get_context_data(self, **kwargs):
#         ctx = {}
#         ctx['loggedIn'] = False
#         if self.request.user.is_authenticated:
#             ctx['loggedIn'] = True
#         return ctx


class SignUpView(TemplateView):
    template_name = 'pat/register.html'

    def get_context_data(self, **kwargs):
        ctx = super(SignUpView, self).get_context_data(**kwargs)
        ctx['user_form'] = UserForm(prefix='user')
        ctx['profile_form'] = ProfileForm(prefix='profile')
        ctx['patient_form'] = PatientForm(prefix='patient')
        print(ctx)
        return ctx

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, prefix='user')
        patient_form = PatientForm(request.POST,prefix='patient')
        profile_form = ProfileForm(request.POST, request.FILES, prefix='profile')
        if profile_form.is_valid() and user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            patient = patient_form.save(commit=False)
            user.save()
            profile.user = user
            profile.save()
            patient.user = profile
            # patient.doctor_id = patient_form 
            patient.save()
            return HttpResponse("Signed Up!<br><a href='/'>Go to home</a>")
        else:
            return HttpResponse("Error : <a href='/signup'>Try again</a>!")


class LoginView(TemplateView):
    template_name = 'pat/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('patients:patient-homepage')
            else:
                return HttpResponse('Error: User authentication error <a href="/login"">Try again</a>')
        else:
            return HttpResponse('Error: Username or password is empty <a href="/login">Try again</a>')


class LogoutView(View, LoginRequiredMixin):
    def get(self, request):
        logout(request)
        return redirect('/') #redirects to doctors login page will fix that
