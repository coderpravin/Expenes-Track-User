from django.shortcuts import render, redirect
from .models import Category,Expenses
from .forms import UserForm,UserLoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib import messages
# Create your views here.

def category_home(request):
    catogories = Category.objects.all()
    context = {'categories': catogories}
    return render(request, 'expenses/category_home.html', context)

def category_page(request):
    categories = Category.objects.all()     
    context = {'categories': categories}
    return render(request, 'expenses/category_page.html', context)

def expenses_home(request):
    expenses = Expenses.objects.all()
    context = {'expenses': expenses}    
    return render(request, 'expenses/expenses_home.html', context)

def userSignup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("User signed up successfully!")
        else:
            return redirect('user-signup')
    else:      
        form = UserForm()
        context = {'form': form}
    return render(request, 'expenses/user_signup.html', context)

def userLogin(request):
    if request.method =="POST":
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            # Authentication logic would go here
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('category-home')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('user-login')   
        else:
            return redirect('user-login')
    else:
        form = UserLoginForm()
        context = {'form': form}    
    return render(request, 'expenses/user_login.html', context)