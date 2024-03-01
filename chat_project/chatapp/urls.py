from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('messages/',views.GetMessage,name='messages'),
    path("signup/",views.Signup,name="signup"),
    path("profile/",views.UpdateProfile,name="profile"),
    path('loguser/',views.loguser,name='loguser'),
    path('quite_status/',views.quite,name='quite_status')
    
] 