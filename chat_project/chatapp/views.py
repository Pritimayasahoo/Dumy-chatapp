from django.shortcuts import render, redirect
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
                user=user, name=name, mail=email)
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


def UpdateProfile(request):
    if request.method == "POST":

        user = request.user
        profile = Profile.objects.get(user=user)

        if request.FILES.get('profilepic'):
            image = request.FILES.get('profilepic')

        else:
            image = profile.profileimg
        about = request.POST["about"]

        profile.profileimg = image
        profile.about = about
        profile.save()

        return redirect('/')
    return render(request, 'profile.html')


@login_required(login_url='/loguser/')
def home(request):

    my_profile = Profile.objects.filter(user=request.user).first()

    all_profiles = Profile.objects.exclude(id=my_profile.id)

    context = {
        'all_profiles': all_profiles,
        'my_profile': my_profile,
    }

    return render(request, 'home.html', context)


@login_required(login_url='/loguser/')
def GetMessage(request):

    Other_id = request.GET.get('other_id')

    Other_profile = Profile.objects.get(id=Other_id)
    Own_profile = Profile.objects.get(user=request.user)

    Recent_gp = Group.objects.filter(
        users=Other_profile).filter(users=Own_profile).first()

    Chats = Chat.objects.filter(group=Recent_gp).all()
    Chats = serialize('json', Chats)

    Chats = json.loads(Chats)

    data = {
        'Chats': Chats,

    }
    return JsonResponse(data)
