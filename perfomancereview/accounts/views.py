from django.shortcuts import render

# Create your views here.
from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout as auth_logout

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('employees')
        else:
            messages.info(request, "Wrong username or password")
            return redirect('login')
    else:
        return render(request, 'registration/login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')
