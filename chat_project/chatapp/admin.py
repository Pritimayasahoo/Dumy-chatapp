from django.contrib import admin
from . models import Chat,Group,Profile
from django.contrib.auth.models import User
admin.site.register(Chat)
admin.site.register(Group)
admin.site.register(Profile)
#admin.site.register(User)
