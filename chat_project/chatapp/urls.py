from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('messages/',views.GetMessage,name='messages'),
    path("signup/",views.Signup,name="signup"),
    path("profile/",views.UpdateProfile,name="profile")
] 