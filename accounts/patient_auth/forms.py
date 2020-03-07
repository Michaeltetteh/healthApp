
from django import forms
from django.contrib.auth.models import User
from django.forms.models import ModelForm

from accounts.models import UserProfile
from patients.models import Patient
from doctors.models import Doctor


class ProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ('gender',)


class UserForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    # include another password field for validation

    class Meta:
        model = User
        fields = ('username','first_name','last_name', 'password', 'email')

    def save(self, commit=True):
        new_user = User.objects.create_user(self.cleaned_data['username'],
                                            self.cleaned_data['email'],
                                            self.cleaned_data['password'])
        if commit:
            new_user.save()
        return new_user


class PatientForm(ModelForm):
    # alldoctors = forms.ModelChoiceField(queryset=Doctor.objects.all())
    class Meta:
        model = Patient
        fields = ('doctor_id','device_serial')
