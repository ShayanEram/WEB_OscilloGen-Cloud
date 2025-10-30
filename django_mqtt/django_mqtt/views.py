import json
from django.http import JsonResponse
from django.http import HttpResponse
from django_mqtt.mqtt import client as mqtt_client

def index(request):
    return HttpResponse("MQTT Django server is running")

def publish_message(request):
    data = json.loads(request.body)
    rc, mid = mqtt_client.publish(data['topic'], data['msg'])
    return JsonResponse({"code": rc})
