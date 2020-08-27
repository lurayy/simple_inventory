from django.urls import path

from . import consumer

websocket_urlpatterns = [
    path('backup/create/progress', consumer.ProgressBarConsumer)
]