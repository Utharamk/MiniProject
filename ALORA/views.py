from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout

from .models import *
from django.http import HttpResponse
import random
from django.core.mail import send_mail
from django.contrib import messages
import stripe
from django.conf import settings 

stripe.api_key = settings.STRIPE_SECRET_KEY

def stripe_payments(request,id):
    try:
        data=Bookings.objects.get(id=id)
        total_amount = data.total_payment

        intent = stripe.PaymentIntent.create(
            amount=int(total_amount*100),
            currency="usd",
            metadata={"data":data.id,"user_id":request.user.id},

        )
        context = {
            'client_secret': intent.client_secret,
            'STRIPE_PUBLISHABLE_KEY': settings.STRIPE_PUBLISHABLE_KEY,
            'total_amount':total_amount,
            'data':data,
        }
        return render(request,'stripe_payments.html',context)
    except Bookings.DoesNotExist:
        return redirect(user_view_booking)
def send_otp(email):
    otp=random.randint(100000,999999)
    
    send_mail(
        'Your OTP Code',''
        f'Your OTP code is: {otp}',
        'utharamk13@gmail.com',
        [email],
        fail_silently=False,
    )
    return otp

def password_reset_request(request):
    if request.method =='POST':
        email=request.POST['email']
        try:
            user = User.objects.get(email=email)
            print("--------------------")
            otp=send_otp(email)

            context={
                "email":email,
                "otp": otp,
            }
            return render(request,'forgot_password2.html',context)
        
        except User.DoesNotExist:
            messages.error(request,'Email address not found.')
            return render(request,'forgot_password1.html',{'error':'not valid'})
    else:
        return render(request,'forgot_password1.html')
    return render(request,'forgot_password1.html')

def verify_otp(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        otpold=request.POST.get('otp1')
        otp=request.POST.get('otp2')

        if otpold==otp:
            context={
                'otp' : otp,
                'email' : email
            }
            return render(request,'forgot_password3.html',context)
        else:
            messages.error(request,"Invalid OTP")
    return render(request,'forgot_password2.html')

def set_new_password(request):
    if request.method == 'POST':
        email=request.POST.get('email')
        new_password=request.POST.get('password1')
        confirm_password=request.POST.get('password2')
        if new_password==confirm_password:
            try:
                user=User.objects.get(email=email)
                
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password has been reset successfully')
                return redirect(user_login)
            except User.DoesNotExist:
                messages.error(request,'Password does not match')
        return render(request,'forgot_password3.html',{'email':email})
    return render(request,'forgot_password3.html',{'email':email})


def index(request):
   return render(request,'index.html')

# Create your views here.
def user_registration(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        if User.objects.filter(email=email).exists():
         return render(request,'registration.html',{'error':'Email already exists'})
        phone_no=request.POST.get('no')
        if User_details.objects.filter(phone_number=phone_no).exists():
           return render (request,'registration.html',{'error':'phone no already exists'})
        gender=request.POST.get('gender')
        address=request.POST.get('address')
        username=request.POST.get('uname')
        if User.objects.filter(username=username).exists():
           return render (request,'registration.html',{'error':'username already exists'})
        
        password=request.POST.get('password')
        confirmpassword=request.POST.get('cpass')
        if password!=confirmpassword:
           return render(request,'registration.html',{'error':'password not matching'})
        data=User.objects.create_user(first_name=name,username=username,password=password,email=email)
        data.save()
        data1=User_details.objects.create(user_id=data,phone_number=phone_no,gender=gender,address=address)
        data1.save()
        return redirect(user_login)
    else:
       return render(request,'registration.html')
    
def user_login(request):
   if request.method == "POST":
      username=request.POST.get('uname')
      password=request.POST.get('password')
      data=authenticate(username=username,password=password)
      admin_user=authenticate(request,username=username,password=password)
      if admin_user is not None and admin_user.is_staff:
         login(request,admin_user)
         return redirect('adminhome')   
      elif data  is not None:
         login(request,data)
         return redirect('userhome')
      else:
         return HttpResponse('invalid username or password')
   else:
      return render(request,'login.html')
   
def user_home(request):
   return render(request,'user_home.html')   

def view_user(request):
    user=User.objects.get(id=request.user.id)
    val=User_details.objects.get(user_id=user.id)
    return render(request,'viewuser.html',{'data':val})

def edit(request):
    data=User.objects.get(id=request.user.id)
    user=User_details.objects.get(user_id=data.id)
    if request.method == 'POST':
        user.user_id.first_name=request.POST['name']
        user.user_id.email=request.POST['email']
        user.phone_number=request.POST['phone_number']
        user.gender=request.POST['gender']
        user.address=request.POST['address']
        user.user_id.save()
        user.save()
        return redirect('viewuser')
    else:
        return render(request,'edituser.html',{'data':user})
    
def Booking(request):
    data=Bookings.objects.all()  

def logout_view(request):
    logout(request)
    context = {'success_message': 'You have been logged out successfully.'}
    return render(request, 'login.html',context)   
def booking(request):
    data=User.objects.get(id=request.user.id)
    halls=Halls.objects.all()
    foods=Food.objects.all()
    decorations=Decoration.objects.all()
    if request.method == 'POST':
        eventdate=request.POST['date']
        hall=request.POST['hall']
        food=request.POST['f']
        food_id=request.POST.get('food')
        no_of_people=request.POST['people_num']
        photography=request.POST['photography']
        decoration=request.POST['decoration']
        decoration_id=request.POST.get('decoration_model')
        check_date=Bookings.objects.filter(hall_id=hall,event_date=eventdate).exists()
        if check_date:
            return HttpResponse('hall already booked!')
        if food == "yes":
            food=True
        else:
            food=False
        if decoration == "yes":
            decoration=True
        else:
            decoration=False
        if no_of_people == "":
            no_of_people=0
        no_of_people=int(no_of_people)
        hall_amount=0
        food_amount=0
        photography_amount=0
        decoration_amount=0
        t_amount=0
        h=Halls.objects.get(id=hall)
        hall_amount=h.price_per_day
        f=None
        d=None
        if food_id:
            f=Food.objects.get(id=food_id)
            food_amount=no_of_people*f.food_price
        if photography == 'yes':
            photography_amount=10000
        if decoration_id:
            d=Decoration.objects.get(id=decoration_id)
            decoration_amount=d.decoration_price
        t_amount=hall_amount+photography_amount+decoration_amount+food_amount
        if food_id and decoration_id :
            obj=Bookings.objects.create(event_date=eventdate,user_id=data,hall_id=h,photography=photography,food_value=food,food=f,no_of_people=no_of_people,decoration_value=decoration,decoration=d,photography_cost=photography_amount,total_payment=t_amount)
            obj.save()
        else:
            obj=Bookings.objects.create(event_date=eventdate,user_id=data,hall_id=h,photography=photography,food_value=food,no_of_people=no_of_people,decoration_value=decoration,photography_cost=photography_amount,total_payment=t_amount)
            obj.save()
        return redirect(user_view_booking)
    else:
        return render(request,'booking.html',{'data':halls,'foods':foods,'decoration':decorations})
    
def user_view_booking(request):
    user=User.objects.get(id=request.user.id)
    booking=Bookings.objects.filter(user_id=user)
    for i in booking:
        print(i.event_status)
    return render(request,'user_view_booking.html',{'x':booking})



def accept_reject_booking(request,id):
    data=Bookings.objects.get(id=id)
    if request.method == 'POST':
        value=request.POST.get('Status')
        if value == 'Accept':
            data.event_status='Accept'
        elif value == 'Reject':
            data.event_status='Reject'
        data.save()
        return redirect(admin_view_booking)
    return redirect(admin_view_booking)
 




# admin/......................

def admin_home(request):
   return render(request,'admin_home.html')   

def user_details(request):
   data=User_details.objects.all()
   return render(request,'user_details.html',{'data':data})

def view_hall(request):
   data = Halls.objects.all()
   return render(request,'view_hall.html',{'data':data})

def add_hall(request):
   if request.method =="POST":
      hall_name=request.POST.get('hall_name')
      location=request.POST.get('location')
      capacity=request.POST.get( 'capacity')
      price_per_day=request.POST.get('price_per_day')
      photo_url=request.FILES['photo_url']
      hall_description=request.POST.get('hall_description')
      data=Halls.objects.create(hall_name=hall_name,
                               location=location,
                               capacity=capacity,
                               price_per_day=price_per_day,
                               photo_url=photo_url,
                               hall_description=hall_description)
      data.save()
      return redirect(view_hall)
   else:
      return render(request,'add_hall.html')
   
def food(request):
   data=Food.objects.all()
   return render(request,'food.html',{'data':data})

def add_food(request):
    if request.method=='POST':
        name=request.POST['name']
        image=request.FILES['image']
        price=request.POST['price']
        val=Food.objects.create(food_name=name,food_image=image,food_price=price)
        val.save()
        return redirect('food')
    else:
        return render(request,'add_food.html')
      


def decoration_details(request):
    data=Decoration.objects.all()
    return render(request,'decoration_details.html',{'data':data})

def add_decoration(request):
    if request.method == 'POST':
        name=request.POST['name']
        price=request.POST['price']
        image=request.FILES['image']
        obj=Decoration.objects.create(decoration_name=name,decoration_price=price,decoration_image=image)
        obj.save()
        return redirect(decoration_details)
    return render(request,'add_decoration.html')

def admin_view_booking(request):
    book=Bookings.objects.all()
    return render(request,'admin_view_booking.html',{'data':book})

