import paho.mqtt.client as mqtt
from django.conf import settings
from telemetry.models import Telemetry
from telemetry.models import WaveformSample

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe("django/mqtt")
    else:
        print("Bad connection. Code:", rc)

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    
    print(f"Received on {msg.topic}: {payload}")
    Telemetry.objects.create(topic=msg.topic, payload=payload)

    if topic == "gateway/001/telemetry/waveform":
        try:
            value = float(payload)
            WaveformSample.objects.create(value=value)
        except ValueError:
            print("Invalid waveform sample:", payload)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(settings.MQTT_SERVER, settings.MQTT_PORT, settings.MQTT_KEEPALIVE)
