from django.shortcuts import render, redirect, HttpResponse
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Group, Chat, Profile
from django.db.models import Q
from django.core.serializers import serialize
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
import json
import email.utils as email_utils
from django.contrib.auth.hashers import check_password
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
import asyncio
import datetime
import pytz


def page_not_found(request, exception):
    return render(request, '404.html')


def Signup(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        name = request.POST["name"]
        if User.objects.filter(username=email):
            messages.info(request, "This user already exist")
            return redirect("/signup/")
        else:

            user = User.objects.create_user(username=email, password=password)
            user_profile = Profile.objects.create(
                user=user, name=name, mail=email, last_seen=timezone.now())
            user_log = auth.authenticate(username=email, password=password)
            auth.login(request, user_log)

            return redirect("/profile/")
    return render(request, "signup.html")


def loguser(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if not email or not password:
            messages.info(request, 'Please Fill All Fields')
            return redirect('/loguser/')

        # Normalize Email
        parsed_email = email_utils.parseaddr(email)[1]
        email = parsed_email.lower()
        user = User.objects.filter(username=email).first()
        # If User Already Exist Then Login User
        if user and check_password(password, user.password):
            my_user = auth.authenticate(username=email, password=password)
            auth.login(request, my_user)
            return redirect('/')
        else:
            messages.info(request, 'PASSWORD OR EMAIL ID IS WRONG')
            return redirect('loguser')
    return render(request, 'login.html')


@login_required(login_url='/loguser/')
def create_profile(request):
    return render(request, "profile.html")


@login_required(login_url='/loguser/')
def SaveProfile(request):
    if request.method == "POST":

        user = request.user
        profile = Profile.objects.get(user=user)

        text_data = request.POST.get("text_data")
        image_data = request.FILES.get("image_data")
        
        text_data=text_data if text_data else profile.name

        profile.profileimg = image_data
        profile.name = text_data

        profile.save()

        return JsonResponse({"message": "Success done"})
    return JsonResponse({'error': 'Something went wrong'}, status=401)


@login_required(login_url='/loguser/')
def home(request):

    current_profile = Profile.objects.filter(user=request.user).first()
    current_profile.online_status = True
    current_profile.last_seen = None
    current_profile.save()
    filtered_groups = Group.objects.filter(users=current_profile)

    all_profiles = Profile.objects.exclude(id=current_profile.id)

    context = {
        'all_profiles': all_profiles,
        'my_profile': current_profile,
    }

    message = {
        'msg': "Online",
        'type': "status_message"
    }

    message_json = json.dumps(message)
    channel_layer = get_channel_layer()
    for group in filtered_groups:
        async_to_sync(channel_layer.group_send)(
            group.name,
            {
                'type': 'chat.message',
                'message': message_json
            }
        )

    return render(request, 'home.html', context)


@login_required(login_url='/loguser/')
def GetMessage(request):

    Other_id = request.GET.get('other_id')

    Other_profile = Profile.objects.get(id=Other_id)
    if Other_profile.online_status == True:
        status = "Online"
        status_type = "Online"
    else:
        status = Other_profile.last_seen
        status_type = "Last_seen"

    Own_profile = Profile.objects.get(user=request.user)

    Recent_gp = Group.objects.filter(
        users=Other_profile).filter(users=Own_profile).first()

    Chats = Chat.objects.filter(group=Recent_gp).all()
    Chats = serialize('json', Chats)

    Chats = json.loads(Chats)

    data = {
        'Chats': Chats,
        'active_status': status,
        'status_type': status_type

    }
    return JsonResponse(data)


async def quite(request):
    # Assuming you have some way to get the current user
    current_user = request.user
    # Call the heavy asynchronous function

    # asyncio.run(process_heavy_task(current_user))
    asyncio.create_task(process_heavy_task(current_user))
    # Return the response immediately
    return JsonResponse({'message': 'Processing heavy task initiated'})


async def process_heavy_task(user):
    # Await the ORM query
    current_profile = await database_sync_to_async(Profile.objects.filter)(user=user)
    current_profile = await database_sync_to_async(current_profile.first)()
    current_profile.online_status = False

    # Get the current time in the India time zone
    india_timezone = pytz.timezone('Asia/Kolkata')
    india_time = datetime.datetime.now(india_timezone)
    formatted_time = india_time.strftime('%Y-%m-%d %H:%M:')

    current_profile.last_seen = timezone.now()
    # Await the save operation
    await database_sync_to_async(current_profile.save)()
    # Convert the synchronous ORM call to asynchronous
    filtered_groups = await database_sync_to_async(Group.objects.filter)(users=current_profile)
    message = {
        'msg': str(current_profile.last_seen),
        'type': "offline_message"
    }
    message_json = json.dumps(message)
    channel_layer = get_channel_layer()
    async for group in filtered_groups:
        await channel_layer.group_send(  # Await the group send operation
            group.name,
            {
                'type': 'chat.message',
                'message': message_json
            }
        )
