from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import get_user_model
from .forms import LoginForm
from .forms import SignupForm

def handleLogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
            
        if not User.objects.filter(username=username).exists():
            return HttpResponseRedirect("/registration/login")
        
        user = authenticate(username=username, password=password)
        if user is None:
            return HttpResponseRedirect("/registration/login")
            
        else:
            # if data is succsefully processed we do a http redirect to the main screen
            login(request, user)
            return HttpResponseRedirect("/chat")
    else:
        form = LoginForm()

    return render(request, "login.html", {"form": form})

def handleSignup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            
            firstName = request.POST.get('firstName')
            lastName = request.POST.get('lastName')

            if User.objects.filter(username=username).exists():
                return HttpResponseRedirect("/registration/login")

            # create a user 
            user = User.objects.create_user(username=username, first_name=firstName, last_name=lastName)
            user.set_password(password)

            user.save()
            return HttpResponseRedirect("/registration/login")

    else:
        form = SignupForm()
    
    return render(request, "signup.html", {"form": form})

def handleLogout(request):
    logout(request)

    return HttpResponseRedirect("/registration/login")