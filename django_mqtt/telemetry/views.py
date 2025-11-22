from django.shortcuts import render
from django.http import JsonResponse
from .models import Telemetry
from .models import WaveformSample

from django.views.decorators.csrf import csrf_exempt
from django_mqtt.mqtt import client as mqtt_client

import os
from django.conf import settings

def list_telemetry(request):
    data = list(Telemetry.objects.order_by('-timestamp').values())
    return JsonResponse(data, safe=False)

@csrf_exempt
def functiongen_control(request):
    if request.method == "POST":
        waveform = request.POST.get("waveform")
        frequency = request.POST.get("frequency")
        amplitude = request.POST.get("amplitude")
        offset = request.POST.get("offset")

        base_topic = "gateway/001/commands/functiongen"

        mqtt_client.publish(f"{base_topic}/waveform", waveform)
        mqtt_client.publish(f"{base_topic}/frequency", frequency)
        mqtt_client.publish(f"{base_topic}/amplitude", amplitude)
        mqtt_client.publish(f"{base_topic}/offset", offset)

    return render(request, "telemetry/functiongen.html")

def oscilloscope_view(request):
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "start":
            mqtt_client.publish("gateway/001/commands/oscilloscope", "start")
        elif action == "stop":
            mqtt_client.publish("gateway/001/commands/oscilloscope", "stop")
        elif action == "fft":
            mqtt_client.publish("gateway/001/commands/oscilloscope", "fft")
        elif action == "filter":
            mqtt_client.publish("gateway/001/commands/oscilloscope", "filter")

    samples = WaveformSample.objects.order_by('-timestamp')[:200][::-1]
    values = [s.value for s in samples]
    timestamps = [s.timestamp.strftime("%H:%M:%S.%f")[:-3] for s in samples]
    return render(request, "telemetry/oscilloscope.html", {
        "values": values,
        "timestamps": timestamps
    })


def firmware_update_view(request):
    if request.method == "POST":
        firmware_file = request.FILES["firmware_file"]
        firmware_version = request.POST["firmware_version"]

        filename = firmware_file.name
        filepath = os.path.join(settings.MEDIA_ROOT, filename)

        with open(filepath, "wb") as f:
            for chunk in firmware_file.chunks():
                f.write(chunk)

        # Publish MQTT command
        payload = {
            "version": firmware_version,
            "filename": filename
        }
        mqtt_client.publish("gateway/001/commands/firmware/update", str(payload))

    return render(request, "telemetry/firmware_update.html")

def about_view(request):
    return render(request, "telemetry/about.html")