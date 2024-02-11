from django.urls import path
from . import consumers
websocket_urlpatterns=[
    path('ws/ac/',consumers.Myasyncconsumer.as_asgi()),
]