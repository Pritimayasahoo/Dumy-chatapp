"""
ASGI config for chat_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
import chatapp.routing
from channels.auth import AuthMiddlewareStack
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chat_project.settings')
print("come to asgi")
application = ProtocolTypeRouter(
    {
        'http':get_asgi_application(),
        'websocket':AuthMiddlewareStack(URLRouter(chatapp.routing.websocket_urlpatterns)),
    }
)
