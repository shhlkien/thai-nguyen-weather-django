from django.db import models

class Weather(models.Model):

    get_time = models.CharField(max_length = 8)
    location = models.CharField(max_length = 50)
    weather = models.TextField()
