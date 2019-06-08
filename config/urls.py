from django.contrib import admin
from django.urls import path
import station.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', station.views.home, name = 'home'),
]
