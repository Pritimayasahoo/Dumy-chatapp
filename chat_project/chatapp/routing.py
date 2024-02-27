from django.urls import path
from . import consumers
websocket_urlpatterns=[
    path('ws/ac/<int:Otherid>/',consumers.Myasyncconsumer.as_asgi()),
]