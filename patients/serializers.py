# from django.contrib.auth.models import User, Group
from .models import PulseModel
from rest_framework import serializers


class pulseserializer(serializers.ModelSerializer):
    class Meta:
        model = PulseModel
        fields = '__all__' #('date','device','pulse_bpm')

    def create(self, validated_data):
        new_BPM = PulseModel(
            #date = datetime.datetime.now(),
            # date = validated_data['date'],
            device_serial_number = validated_data['device'],
            pulse_bpm = validated_data['pulse_bpm'],
            temperature = validated_data['temperature'],
            )

        new_BPM.save()

        return new_BPM

