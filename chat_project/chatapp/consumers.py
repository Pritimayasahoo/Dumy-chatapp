from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from .models import Group, Chat, Profile
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
import asyncio
import json
# from asgiref.sync import sync_to_async


class Myasyncconsumer(AsyncConsumer):

    async def websocket_connect(self, event):
        Otherid = self.scope['url_route']['kwargs']['Otherid']

        await self.send(
            {
                'type': 'websocket.accept'
            }
        )
        if Otherid:
            self.other_profile = await database_sync_to_async(Profile.objects.get)(id=Otherid)
            self.owner_profile = await database_sync_to_async(Profile.objects.get)(user=self.scope["user"])

            filtered_groups = await database_sync_to_async(Group.objects.filter)(users=self.owner_profile)
            filtered_groups = await database_sync_to_async(filtered_groups.filter)(users=self.other_profile)

            exist = await database_sync_to_async(filtered_groups.exists)()

            if exist:
                self.new_group = await database_sync_to_async(filtered_groups.first)()
                self.group_name = self.new_group.name

            else:
                # If no group exists, create a new group with both users
                self.group_name = str(self.owner_profile.id) + \
                    "-"+str(self.other_profile.id)

                self.new_group = await database_sync_to_async(Group.objects.create)(name=self.group_name)

                await database_sync_to_async(self.new_group.users.add)(self.owner_profile, self.other_profile)

            await self.channel_layer.group_add(self.group_name, self.channel_name)

    async def websocket_receive(self, event):

        data = json.loads(event['text'])
        
        if data['type']=="Normal_message":
            await database_sync_to_async(Chat.objects.create)(context=data['msg'], user=self.owner_profile, group=self.new_group)

        await self.channel_layer.group_send(self.group_name,
                                            {
                                                'type': 'chat.message',
                                                'message': event['text']
                                            },

                                            )

    async def chat_message(self, event):

        await self.send(
            {
                'type': 'websocket.send',
                'text': event['message']
            }
        )

    async def websocket_disconnect(self, event):
        try:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
    
            raise StopConsumer()
        except:
            raise StopConsumer()
