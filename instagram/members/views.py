from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User





# Create your views here.
def login_user(request):

    # if request.method == 'POST':
    #     username = request.POST['username']
    #     password = request.POST['password']
    username = 'priyanka'
    password = 'chithira'
    user = authenticate(request,username=username,password=password)
    if user is not None:
        login(request, user)
            
        return JsonResponse({'message':'login successful'})
            # return redirect('home')
    else:
        return redirect('login')


def logout_user(request):
    logout(request)
    messages.success(request,("User logged out successfully"))
    return redirect('home')

    # return render(request, 'authenticate/login.html', {})

def register_user(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username=username, password=password)
            user = authenticate(username=username,password=password)
            login(request, user)
        except Exception as e:
            raise ValueError("Invalid parameters")
            
        return JsonResponse({'message':'registration successful'})
          