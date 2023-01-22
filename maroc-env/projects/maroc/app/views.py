from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login

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
            return redirect('signup')
    return render(request,'signin.html')

def signup(request):
    if request.method == "POST": 
        email=request.POST['email']
        password=request.POST['password']
        username=email.split("@", 1)[0]
        confirmpassword=request.POST['confirmpassword']
        myuser=User.objects.create_user(username,email,password)
        myuser.save()
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