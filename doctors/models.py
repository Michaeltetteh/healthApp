from django.db import models
# from django.contrib.auth.models import User
from accounts.models import UserProfile
# from patients.models import Patient


class Doctor(models.Model):
    DOCTOR_SPECIALITY = (
	    ('Anesthesiologists‎','Anesthesiologists'),
	    ('Cardiologists‎','Cardiologists‎'),
	    ('Coroners‎','Coroners‎'),
	    ('Dentists‎','Dentists‎'),
	    ('Dermatologists‎','Dermatologists‎'),
	    ('Diabetologists‎','Diabetologists‎'),
	    ('Emergencyphysicians‎','Emergencyphysicians‎'),
	    ('Endocrinologists‎','Endocrinologists‎'),
	    ('Euthanasia','Euthanasia'),
	    ('Gastroenterologists‎','Gastroenterologists‎'),
	    ('Generalpractitioners‎','Generalpractitioners‎'),
	    ('Gynaecologists‎','Gynaecologists‎'),
	    ('Hematologists‎','Hematologists‎'),
	    ('Immunologists‎','Immunologists‎'),
	    ('Neurologists‎','Neurologists‎'),
	    ('Neurosurgeons‎','Neurosurgeons‎'),
	    ('Pathologists‎','Pathologists‎')
    )

    user = models.OneToOneField(UserProfile, primary_key=True,on_delete=models.CASCADE)
    # userF = models.OneToOneField(User,on_delete=models.CASCADE)
    specialty = models.CharField(max_length=30)#,choices=DOCTOR_SPECIALITY)
    # patients  = models.models.ForeignKey(Patient,on_delete=models.CASCADE)

    def __str__(self):
        return self.user.user.username + " -- " + self.user.user.email