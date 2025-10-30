from django.shortcuts import render
from django.http import JsonResponse
from .models import Telemetry

def list_telemetry(request):
    data = list(Telemetry.objects.order_by('-timestamp').values())
    return JsonResponse(data, safe=False)
