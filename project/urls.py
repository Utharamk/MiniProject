"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ALORA import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index),
    path('reg',views.user_registration,name='reg'),
    path('log',views.user_login,name='log'),


    path('userhome',views.user_home,name='userhome'),
    path('viewuser',views.view_user,name='viewuser'),
    path('logout',views.logout_view,name='logout'),
    path('booking',views.booking,name='booking'),
    path('userviewbooking',views.user_view_booking,name='userviewbooking'),

    path('resetpassword',views.password_reset_request,name='resetpassword'),
    path('verifyotp',views.verify_otp,name='verifyotp'),
    path('newpassword',views.set_new_password,name='newpassword'),

    path('viewd',views.decoration_details,name='viewd'),
    path('addd',views.add_decoration,name='addd'),

    path('food',views.food,name='food'),
    path('ad_fud',views.add_food,name='ad_fud'),

    path('edit',views.edit,name='edit'),

    path('adminhome',views.admin_home,name='adminhome'),
    path('userdetails',views. user_details,name='userdetails'),
    path('viewhall',views.view_hall,name='viewhall'),
    path('addhall',views.add_hall,name='addhall'),
    path('adminviewbooking',views.admin_view_booking,name='adminviewbooking'),
    path('acceptrejectbooking/<int:id>',views.accept_reject_booking,name='acceptrejectbooking'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)