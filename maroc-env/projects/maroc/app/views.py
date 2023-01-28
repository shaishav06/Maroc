from base64 import urlsafe_b64decode
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from maroc import settings
from django.core.mail import send_mail,EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from .helper import send_forgot_password_mail
from .models import Profile


# Create your views here.
def index(request):
    return render(request,'index.html')

def signin(request):
    if 'username' in request.session:
        return redirect('home')
    if(request.method == "POST"):
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            request.session['username'] = username
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,"Wrong Credentials !")
            return redirect('signin')
    return render(request,'signin.html')

def signup(request):
    if request.method == "POST": 
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        # username=email.split("@", 1)[0]
        confirmpassword=request.POST['confirmpassword']

        if User.objects.filter(username=username):
            messages.error(request,"Username already exists!")
            return redirect('signin')
        
        if User.objects.filter(email=email):
            messages.error(request,"Email Account already exists!")
            return redirect('signin')
        
        if password != confirmpassword:
            messages.error(request,"Password didn't match !")

        if not username.isalnum():
            messages.error(request,"Username must be Alpha-Numeric !")
            return redirect('signin')
        
        
        myuser=User.objects.create_user(username,email,password)
        myuser.is_active = False
        myuser.save()
        # messages.success(request,"Your Account has been successfully created. Please Login Here :)")

        # Welcome Email

        subject = "Welcome to Maroc : A Health Application"
        message = "Hello "+ myuser.username +",\n\n" + "Welcome to Maroc, a nutrition consulting website based in India that aims to help clients manage chronic health issues such as weight gain, diabetes, PCOS, and thyroid through personalized diet protocols.\n\nThank you for visiting our website.\n\nWe have also sent you a confidential email, please confirm your email address in order to activate your account.\n\n"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        # return redirect('signin')
    
        # Email Confimation

        current_site = get_current_site(request)
        email_subject = "Confirm your email @ Maroc - A Health Application"
        message2 = render_to_string('email_confirmation.html',{
            'name' : myuser.username,
            'domain' : current_site.domain                                      
        })
        email = EmailMessage(
            email_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email],
        )
        email.fail_silently = True
        email.send()

        return redirect('signin')
        
    
    return render(request,'signup.html')

def home(request):
    if 'username' in request.session:
        context = {
            'username':request.session['username']
        }
        return render(request,'home.html',context)
    return redirect(signin)

def logout(request):
    if 'username' in request.session:
        request.session.flush()
    return redirect('signin')

def activate(request,uname):

    try:
        myuser = User.objects.get(username=uname)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser=None

    if myuser is not None:
        myuser.is_active=True
        myuser.save()
        login(request,myuser)
        return redirect('home')
    else:
        return render(request,'activation_failed.html')

import uuid
def forgot(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            print(username)
            if not User.objects.filter(username=username).first():
                messages.success(request,'Not User found with this Username!')        
                return redirect(forgot)
            
            user_obj = User.objects.get(username=username)
            print(username)
            token = str(uuid.uuid4())
            print(username)
            profile_obj = Profile.objects.get(user=user_obj)
            profile_obj.forgot_password_token = token
            profile_obj.save()
            print(username)
            send_forgot_password_mail(user_obj.email,token)
            print(username)

            messages.success(request,'An email is sent')
            return redirect(forgot)
    except Exception as e:
        print(e)
    return render(request,'forgot.html')

def changepassword(request,token):
    context = {}
    try:
        profile_obj = User.objects.get(forgot_password_token = token).first()
        context = {'user_id' : profile_obj.user.id}

        print(profile_obj)

        if request.method =='POST':
            new_pass = request.POST.get('password')
            con_new_pass = request.POST.get('con_password')
            user_id = request.POST.get('user_id')

            if user_id is None:
                messages.success(request,'No User Found!!!')
                return redirect(f'changepassword/{token}')

            if new_pass != con_new_pass:
                messages.success(request,'Both Password should be same')
                return redirect(f'changepassword/{token}')

            user_obj = User.objects.get(id=user_id)
            user_obj.set_password(new_pass)
            user_obj.save()
            return redirect('login')

    except Exception as e:
        print(e)
    return render(request,'changepassword.html')

def pcos(request):
    return render(request,'pcos.html')

def weightloss(request):
    return render(request,'weightloss.html')