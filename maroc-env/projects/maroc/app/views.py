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