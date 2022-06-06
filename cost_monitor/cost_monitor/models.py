from django.db import models


class Journey(models.Model):
    start = models.CharField(max_length=50)
    end = models.CharField(max_length=50)
    day = models.DateField(auto_now_add=False)
    earliest_start_time = models.TimeField(auto_now_add=False)
    latest_start_time = models.TimeField(auto_now_add=False)

    def __str__(self) -> str:
        return f"{self.start} -> {self.end} @ {self.day}" 

class Connection(models.Model):
    journey = models.ForeignKey(Journey, related_name="connections", on_delete=models.RESTRICT)
    start_time = models.TimeField(auto_now_add=False)
    end_time = models.TimeField(auto_now_add=False)

    def __str__(self) -> str:
        return f"{self.journey} @ {self.start_time}"


class Fare(models.Model):
    connection = models.ForeignKey(Connection, related_name="fares", on_delete=models.RESTRICT)
    timestamp = models.DateTimeField(auto_now_add=True)
    fare = models.FloatField()

    def __str__(self) -> str:
        return f"{self.connection} for {self.fare} found at {self.timestamp}"
