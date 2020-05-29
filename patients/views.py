from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .serializers import pulseserializer

import datetime
import json

from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    return render(request, "index.html") #HttpResponse('Connected')



@csrf_exempt
def post_pulse(request):
    if request.method == "POST":
        # print('Connected to view...')
        # received_data = json.loads(request.body)
        received_json_data = json.loads(request.body.decode("utf-8"))
        print(received_json_data)
        print(received_json_data['device'])
        print(received_json_data['pulse_bpm'])

        serializer = pulseserializer(
            data={ #Must match model
                'date': datetime.datetime.now(),
                'device': received_data['device'],
                'pulse_bpm': received_data['pulse_bpm'],
                })

        if serializer.is_valid():
            serializer.save()
            return HttpResponse("Uploaded")
        else:
            print("Data not valid")
            return HttpResponse("Upload failed")

        return HttpResponse()
    else:
        return HttpResponse('')

#TODO change HttpResponse to JsonResponse
