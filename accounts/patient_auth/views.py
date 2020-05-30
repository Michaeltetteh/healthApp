from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.views.generic.base import View

from .forms import UserForm,ProfileForm,PatientForm
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from django.core import serializers
from django.http import HttpResponse, JsonResponse


# class Index(TemplateView):
#     template_name = 'patient/index.html'

#     def get_context_data(self, **kwargs):
#         ctx = {}
#         ctx['loggedIn'] = False
#         if self.request.user.is_authenticated:
#             ctx['loggedIn'] = True
#         return ctx


# class SignUpView(TemplateView):
#     template_name = 'pat/register.html'

#     def get_context_data(self, **kwargs):
#         ctx = super(SignUpView, self).get_context_data(**kwargs)
#         ctx['user_form'] = UserForm(prefix='user')
#         ctx['profile_form'] = ProfileForm(prefix='profile')
#         ctx['patient_form'] = PatientForm(prefix='patient')
#         print(ctx)
#         return ctx

#     def post(self, request, *args, **kwargs):
#         user_form = UserForm(request.POST, prefix='user')
#         patient_form = PatientForm(request.POST,prefix='patient')
#         profile_form = ProfileForm(request.POST, request.FILES, prefix='profile')
#         if profile_form.is_valid() and user_form.is_valid() and patient_form.is_valid():
#             user = user_form.save(commit=False)
#             profile = profile_form.save(commit=False)
#             patient = patient_form.save(commit=False)
#             user.save()
#             profile.user = user
#             profile.save()
#             patient.user = profile
#             # patient.doctor_id = patient_form 
#             patient.save()
#             return HttpResponse("Signed Up!<br><a href='/'>Go to home</a>")
#         else:
#             return HttpResponse("Error : <a href='/signup'>Try again</a>!")


# class LoginView(TemplateView):
#     template_name = 'pat/login.html'

#     def post(self, request, *args, **kwargs):
#         username = request.POST.get('username', False)
#         password = request.POST.get('password', False)
#         if username and password:
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('patients:patient-homepage')
#             else:
#                 return HttpResponse('Error: User authentication error <a href="/login"">Try again</a>')
#         else:
#             return HttpResponse('Error: Username or password is empty <a href="/login">Try again</a>')


# class LogoutView(View, LoginRequiredMixin):
#     def get(self, request):
#         logout(request)
#         return redirect('/') #redirects to doctors login page will fix that


# def login_api(request):
#     return "login"

from .utils import validate_username_and_password,validateEmail
from accounts.models import UserProfile
from patients.models import Patient,PulseModel
from doctors.models import Doctor

@csrf_exempt
def signup_api(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body.decode("utf-8"))

        username = received_json_data.get('username')
        password = received_json_data.get('password')
        confirm_password = received_json_data.get('confirm_password')
        first_name = received_json_data.get('first_name')
        last_name = received_json_data.get('last_name')
        email = received_json_data.get('email')
        gender = received_json_data.get('gender')
        doctors = received_json_data.get('doctors')
        serial_number= received_json_data.get('serial')

        if validate_username_and_password(username,password,confirm_password) == 'valid':
            if validateEmail(email):
                
                user = User.objects.create_user(
                    first_name = first_name,
                    last_name = last_name,
                    username = username,
                    email = email,
                    password = password,
                    )
                
                user_profile =UserProfile.objects.create(
                    user = user,
                    gender = gender
                    )

                doctor_instance = User.objects.get(username=doctors)
                user_prof = UserProfile.objects.get(user=doctor_instance.id)
                doctor = Doctor.objects.get(pk=user_prof.id)

                patient = Patient.objects.create(
                    user = user_profile,
                    doctor_id = doctor,
                    device_serial = serial_number
                    )

                response = json.dumps({'status':'success', 'user':user_profile.id})
            else:
                response = json.dumps({'status':'error','result':"Email not valid"})
        else:
            response = json.dumps({'status':'error','result':"Username/password error"})
    return HttpResponse(response, content_type='application/json')


@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        received_json_data = json.loads(request.body.decode("utf-8"))
        username = received_json_data.get('username')
        password = received_json_data.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:

                user_serial = User.objects.get(pk= user.id)
                user_profile = UserProfile.objects.get(user=user_serial)
                
                response = json.dumps({
                    'status': 'ok', 
                    'user_profile_id': user_profile.id
                    })
            else:
                response = json.dumps({'status': 'error', 'result': "Wrong username or password"})
        else:
            response = json.dumps({'status': 'error', 'result': "Username or password not provided"})
    else:
        response = json.dumps({'status': 'error', 'result': "something went wrong"})

    return HttpResponse(response, content_type='application/json')


def dashboard_api(request,device):
    if request.method == "GET":
        obj = PulseModel.objects.filter(device_serial_number=device)
        data = []
        for i in obj:
            data.append({
                'pulse' : i.pulse_bpm,
                'temperature' : i.temperature,
                'date' : i.date
                })

        return JsonResponse({'status':'ok',"obj":data})

