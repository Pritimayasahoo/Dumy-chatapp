from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from .models import Group,Chat,Profile
from django.db.models import Q
from django.core.serializers import serialize
from django.contrib import messages,auth
#from django.contrib.auth.models
import json
# Create your views here.
#404 page
def page_not_found(request,exception):
    print('something issue',exception)
    return render(request,'404.html')

def Signup(request):
    if request.method=="POST":
        email=request.POST["email"]
        password=request.POST["password"]
        name=request.POST["name"]
        print("got",email,name,password)
        if User.objects.filter(username=email):
            print("user here")
            messages.info(request,"This user already exist")
            print("go")
            return redirect("/signup/")
        else:
            print("user will create")
            user=User.objects.create_user(username=email,password=password)
            user_profile=Profile.objects.create(user=user,name=name,mail=email)
            user_log=auth.authenticate(username=email,password=password)
            auth.login(request,user_log)
            print("profile aslso create")
            return redirect("/profile/")        
    return render(request,"signup.html")   

def UpdateProfile(request):
    if request.method=="POST":
        print("got here")
        user=request.user
        profile=Profile.objects.get(user=user)
        print("it's my profile",profile)
        print("it's my about",profile.about)
        print("it's my img",profile.profileimg)
        if request.FILES.get('profilepic'):
            image=request.FILES.get('profilepic')
            print("image got",image)
        else:
            image=profile.profileimg   
        about=request.POST["about"]   
        print("what if",about) 
        print(profile)
        profile.profileimg=image
        profile.about=about
        profile.save()
        print(profile,"new one")
        return redirect('/')
    return render(request,'profile.html')

def home(request):
    print('go home')
    my_profile=Profile.objects.get(user=request.user)
    all_profiles=Profile.objects.exclude(id=my_profile.id)

    context={
        'all_profiles':all_profiles,
        'my_profile':my_profile
    }
    return render(request,'home.html',context)

def GetMessage(request):
    print('some we get')
    Other_id=request.GET.get('other_id')
    print(Other_id,"id of other")
    Other_profile=Profile.objects.get(id=Other_id)
    Own_profile=Profile.objects.get(user=request.user)
    print(Other_profile,"other person")
    print(request.user,"i am user")
    Recent_gp=Group.objects.filter(users=Other_profile).filter(users=Own_profile).first()
    print(Recent_gp,"gpm")
    Chats=Chat.objects.filter(group=Recent_gp).all()
    Chats=serialize('json',Chats)
    print(Chats,"whats type",type(Chats))
    Chats=json.loads(Chats)
    #print('process on it',Chats,type(Chats))

    
    print('data send')
    print(type(Chats))
    data={
        'Chats':Chats
    }
    return JsonResponse(data) 