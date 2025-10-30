from django.apps import AppConfig


class TelemetryConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'telemetry'

    def ready(self):
        # Import and start MQTT loop here
        from django_mqtt import mqtt
        mqtt.client.loop_start()
