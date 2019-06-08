from django.shortcuts import render
from django.template.response import TemplateResponse
from .models import Weather
import json

def home(req):

    data = Weather.objects.last()
    data.weather = json.loads(data.weather)
    return TemplateResponse(req, 'index.html', {'data': data})