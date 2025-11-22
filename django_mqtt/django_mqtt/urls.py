"""
URL configuration for django_mqtt project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from telemetry import views as telemetry_views
from . import views as project_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path("admin/", admin.site.urls),
    path("", project_views.index, name="index"),
    path("publish", project_views.publish_message, name="publish"),
    path('telemetry/', telemetry_views.list_telemetry, name='telemetry'),
    path('functiongen/', telemetry_views.functiongen_control, name='functiongen'),
    path("oscilloscope/", telemetry_views.oscilloscope_view, name="oscilloscope"),
    path("firmware/", telemetry_views.firmware_update_view, name="firmware"),
    path("about/", telemetry_views.about_view, name="about"),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
