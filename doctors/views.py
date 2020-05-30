from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from patients.models import Patient
from accounts.models import UserProfile

# @login_required

# class HomePage(TemplateView,LoginRequiredMixin):
#     template_name = 'doctor/home.html'

#     def get_context_data(self, **kwargs):

#         ctx = {}
#         ctx['loggedIn'] = False
#         if self.request.user.is_authenticated:
#             ctx['loggedIn'] = True
#         return ctx


@login_required
def HomePage(request,*args,**kwargs):
	# username = None
	# if request.user:
	# 	username = request.user.username
	# 	print(username)

	print(request.user.id)
	user_profile = UserProfile.objects.get(user=request.user)
	print(user_profile.id)
	patients = Patient.objects.filter(doctor_id=user_profile.id)
	print(patients)
	for p in patients:
		print(p.user)
		print(p.device_serial)

	return render(request, "doctor/home.html",context={
		'patients': patients
		})
