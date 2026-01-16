from django.shortcuts import render
from .models import Category
from .forms import UserForm, UserLoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login 
    # Create your views here.

def category_home(request):
    catogories = Category.objects.all()
    context = {'categories': catogories}
    return render(request, 'expenses/category_home.html', context)

def user_signup(request):
    if request.method == "POST":
        form =UserForm(request.POST)
        if form.is_valid():
            user =  form.save(commit=False)
            user.save()
            return HttpResponse("User registered successfully")
        else:
            return HttpResponse("Form is not valid")    
    else:
        form = UserForm()
    context = {'form': form}
    return render(request, 'expenses/user_signup.html', context)

def user_login(request):
    if request.method == "POST":
        form =UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Here you would typically authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponse("User logged in successfully")
            else:
                return HttpResponse("Invalid credentials")
        else:
            return HttpResponse("Form is not valid")
    else:
        form = UserLoginForm()
    context = {'form': form}    
    return render(request, 'expenses/user_login.html', context)

def forgot_password(request):
    return render(request, 'expenses/forgot_password.html')