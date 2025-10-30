import paho.mqtt.client as mqtt
from django.conf import settings

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        client.subscribe("django/mqtt")
    else:
        print("Bad connection. Code:", rc)

def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(settings.MQTT_USER, settings.MQTT_PASSWORD)
client.connect(settings.MQTT_SERVER, settings.MQTT_PORT, settings.MQTT_KEEPALIVE)
