from .models import PulseModel
from rest_framework import viewsets
from .serializers import pulseserializer

class PulseViewSet(viewsets.ModelViewSet):
    queryset = PulseModel.objects.all().order_by('-id')[:30] #TODO Make this Dynamic
    serializer_class = pulseserializer
