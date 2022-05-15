from django.db import models

class Journey(models.Model):
    start = models.CharField(max_length=50)
    end = models.CharField(max_length=50)
    day = models.DateField(auto_now_add=False)
    earliest_start_time = models.TimeField(auto_now_add=False)
    latest_start_time = models.TimeField(auto_now_add=False)


class Connection(models.Model):
    journey = models.ForeignKey(Journey)
    start_time = models.TimeField(auto_now_add=False)
    end_time = models.TimeField(auto_now_add=False)


class Price(models.Model):
    connection = models.ForeignKey(Connection)
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.FloatField()
