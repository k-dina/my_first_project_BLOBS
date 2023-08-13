from django.db import models


class Simulation(models.Model):
    simulation_id = models.CharField(max_length=255)


class Snapshot(models.Model):
    simulation = models.ForeignKey(Simulation, on_delete=models.CASCADE)
    step = models.IntegerField()
    field = models.JSONField()
    blobs = models.JSONField()
    blobs_on_field = models.JSONField()
