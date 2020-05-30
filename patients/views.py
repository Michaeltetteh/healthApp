from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import pulseserializer
from .models import PulseModel,Patient
import datetime
import json
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, "index.html") #HttpResponse('Connected')



@csrf_exempt
def post_vitals(request):
    if request.method == "POST":
        # print('Connected to view...')
        # received_data = json.loads(request.body)
        received_json_data = json.loads(request.body.decode("utf-8"))
        print(received_json_data)

        data = PulseModel.objects.create(
            date = timezone.now,
            device_serial_number = received_json_data['device_serial_number'],
            pulse_bpm = received_json_data['pulse_bpm'],
            temperature = received_json_data['temperature'],
            )

        if data:
            response = JsonResponse({"status":"OK","msg":"Uploaded"})
        else:
            print("Data not valid")
            response = JsonResponse({"status":"FAILED","msg":"Failed"})

        return response
    else:
        return JsonResponse({"status":"NOT FOUND","msg":"method not found"})