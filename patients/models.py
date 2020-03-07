from django.db import models
from doctors.models import Doctor
from accounts.models import UserProfile
# from django.core import validators


class PulseModel(models.Model):

    date = models.DateTimeField(auto_now=False)
    device = models.CharField(max_length=20)
    pulse_bpm = models.FloatField(max_length=5)

    def __str__(self):
    	return self.device 


class Patient(models.Model):
	user = models.OneToOneField(UserProfile, primary_key=True,on_delete=models.CASCADE)
	doctor_id = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	device_serial = models.ForeignKey(PulseModel,on_delete=models.CASCADE,default='')
	
	def __str__(self):
		return self.user.user.username +" -- " + self.user.user.email







    