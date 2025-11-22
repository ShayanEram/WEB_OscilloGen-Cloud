from django.db import models

class Telemetry(models.Model):
    topic = models.CharField(max_length=255)
    payload = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} @ {self.timestamp}"


class WaveformSample(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    value = models.FloatField()

    def __str__(self):
        return f"{self.timestamp}: {self.value}"

