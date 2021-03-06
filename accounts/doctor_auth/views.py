from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect,render
from django.views.generic import TemplateView
from django.views.generic.base import View
from django.urls import reverse


from .forms import ProfileForm,UserForm,DoctorForm

class SignUpView(TemplateView):
    template_name = 'doc/register.html'

    def get_context_data(self, **kwargs):
        ctx = super(SignUpView, self).get_context_data(**kwargs)
        ctx['user_form'] = UserForm(prefix='user')
        ctx['profile_form'] = ProfileForm(prefix='profile')
        ctx['doctor_form'] = DoctorForm(prefix='doctor')
        return ctx

    def post(self, request, *args, **kwargs):
        user_form = UserForm(request.POST, prefix='user')
        doctor_form = DoctorForm(request.POST,prefix='doctor')
        profile_form = ProfileForm(request.POST, request.FILES, prefix='profile')
        if profile_form.is_valid() and user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            profile = profile_form.save(commit=False)
            doctor = doctor_form.save(commit=False)
            user.save()
            profile.user = user
            profile.save()
            doctor.user = profile
            doctor.save()
            redirect_home = reverse('doctor:doctor-homepage')#, kwargs={'message': 'User created','user':user})
            return HttpResponseRedirect(redirect_home)
        else:
            redirect_signup = reverse('accounts:doctor_register')#, kwargs={'message': "form error please check you detials"})
            return HttpResponseRedirect(redirect_signup)


class LoginView(TemplateView):
    template_name = 'doc/login.html'

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse('doctors:doctor-homepage'))
            else:
                redirect_login_page = reverse('accounts:doctor-login')#, kwargs={'message': "form error please check you detials"})
                return HttpResponseRedirect(redirect_login_page)
        else:
            redirect_login_page = reverse('accounts:doctor-login')#, kwargs={'message': "form error please check you detials"})
            return HttpResponseRedirect(redirect_login_page)


class LogoutView(View, LoginRequiredMixin):
    def get(self, request):
        logout(request)
        return redirect('/')
