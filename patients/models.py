from django.db import models
from doctors.models import Doctor
from accounts.models import UserProfile
# from django.core import validators


class Patient(models.Model):
	user = models.OneToOneField(UserProfile, primary_key=True,on_delete=models.CASCADE)
	doctor_id = models.ForeignKey(Doctor,on_delete=models.CASCADE)
	device_serial = models.CharField(max_length=50)
	
	def __str__(self):
		return self.user.user.username +" -- " + self.user.user.email



class PulseModel(models.Model):

    date = models.DateTimeField(auto_now=True)
    device_serial_number = models.CharField(max_length=50)
    pulse_bpm = models.FloatField(max_length=5)
    temperature = models.FloatField(max_length=5)

    def __str__(self):
    	return self.device_serial_number 