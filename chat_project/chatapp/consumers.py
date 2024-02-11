from channels.consumer import AsyncConsumer
from channels.exceptions import StopConsumer
from .models import Group,Chat,Profile
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
import asyncio
import json
from asgiref.sync import sync_to_async
class Myasyncconsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print('connect .... ro server ok')
        print(self.channel_name)
        
        await self.send(
            {
                'type':'websocket.accept'
            }
        )
    
    
    async def websocket_receive(self,event):
        print(event['text'],"this is the 1st receive")
        data=json.loads(event['text'])
        other_id=data['otherid']
        other_profile=await database_sync_to_async(Profile.objects.get)(id=other_id)
        #print(other_user,'it is other one ')
        #owner=self.scope["user"]
        owner_profile=await database_sync_to_async(Profile.objects.get)(user=self.scope["user"])
        #print(owner,"is minemy nmae is",owner.username)
        filtered_groups = await database_sync_to_async(Group.objects.filter)(users=owner_profile)
        filtered_groups= await database_sync_to_async(filtered_groups.filter)(users=other_profile)
        #users__in=[other_user, owner]
        #print(filtered_groups)
        exist=await database_sync_to_async(filtered_groups.exists)()
        print(exist)
        if exist:
           new_group= await database_sync_to_async(filtered_groups.first)()
           self.group_name=new_group.name
           print(self.group_name,'it is exist')
        else:
           # If no group exists, create a new group with both users
           # If no group exists, create a new group with both users
           self.group_name=str(owner_profile.id)+"-"+str(other_profile.id)
           print(self.group_name,"create one")
           new_group = await database_sync_to_async(Group.objects.create)(name=self.group_name)
           print(new_group)
           await database_sync_to_async(new_group.users.add)(owner_profile,other_profile)

        await self.channel_layer.group_add(self.group_name,self.channel_name)
        await database_sync_to_async(Chat.objects.create)(context=data['msg'],user=owner_profile,group=new_group)
        
        await self.channel_layer.group_send(self.group_name,
                                            {
                                                'type':'chat.message',
                                                'message':event['text']
                                            }
                                            )
    async def chat_message(self,event):
            await self.send(
            {
                'type':'websocket.send',
                'text':event['message']
            }
            )    
        
        

    async def websocket_disconnect(self,event):
        try:    
            await self.channel_layer.group_discard(self.group_name,self.channel_name)
            print('disconnect')
            raise StopConsumer()
        except:
            raise StopConsumer()
            
       