from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import PulseModel
from .serializers import pulseserializer
from django.core import serializers
# from rest_framework.views import APIView
# from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt

import datetime
import json

@csrf_exempt
def last_pulse(request,device):
    obj = PulseModel.objects.filter(device_serial_number__icontains=device).order_by('-id')[:1]
    json_serializer = serializers.get_serializer("json")()
    data = json_serializer.serialize(obj, ensure_ascii=False)
    return HttpResponse(data)
@csrf_exempt
def pusle_chart_by_device(request, device, datapoints):

    obj = PulseModel.objects.filter(device_serial_number__icontains=device).order_by('-id')[:datapoints]
    json_serializer = serializers.get_serializer("json")()
    data = json_serializer.serialize(obj,ensure_ascii=False)
    return HttpResponse(data)
@csrf_exempt
def str_test(request,device):
    return HttpResponse(device)
