from django.shortcuts import render, redirect, get_object_or_404
from .models import Category,Expenses
from .forms import UserForm,UserLoginForm
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import random
# Create your views here.

def category_home(request):
    catogories = Category.objects.all()
    context = {'categories': catogories}
    return render(request, 'expenses/category_home.html', context)

def category_page(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    context = {'category': category}
    return render(request, 'expenses/category_page.html', context)

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

def expenses_home(request):
    expenses = Expenses.objects.all()
    context = {'expenses': expenses}    
    return render(request, 'expenses/expenses_home.html', context)

def userSignup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'User signed up successfully! Please login.')
            return redirect('user-login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
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
                return redirect('user-home')
            else:
                messages.error(request, "Invalid username or password.")
                return redirect('user-login')   
        else:
            return redirect('user-login')
    else:
        form = UserLoginForm()
        context = {'form': form}    
    return render(request, 'expenses/user_login.html', context)

def userLogout(request):
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('user-login')   

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
       
        otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
        print(f"OTP for {email}: {otp}")
        
        # Send OTP via email
        subject = 'Password Reset OTP'
        message = f'Your OTP for password reset is: {otp}\n\nThis OTP is valid for 10 minutes.'
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            request.session['reset_email'] = email  # Store email in session
            request.session['reset_otp'] = otp  # Store OTP in session
            messages.success(request, f'OTP sent to your email id: {email}')
            return redirect('verify-otp')
        except Exception as e:
            messages.error(request, f'Error sending email: {str(e)}')
            return redirect('forgot-password')
    return render(request, 'expenses/forgot_password.html')

def verify_otp(request):
    if request.method == "POST":
        otp = request.POST.get('otp')
        session_otp = request.session.get('reset_otp')
        
        if otp == session_otp:
            messages.success(request, 'OTP verified successfully!')
            return redirect('reset-password')
        else:
            messages.error(request, 'Invalid OTP!')
            return redirect('verify-otp')
    return render(request, 'expenses/verify_otp.html')

def reset_password(request):
    if request.method == "POST":
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if new_password != confirm_password:
            messages.error(request, 'Passwords do not match!')
            return redirect('reset-password')
        
        # Get email from session
        email = request.session.get('reset_email')
        if not email:
            messages.error(request, 'Session expired. Please try again.')
            return redirect('forgot-password')
        
        # Update user password in database
        try:
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            messages.success(request, 'Password reset successfully!')
            return redirect('success-password-reset')
        except User.DoesNotExist:
            messages.error(request, 'User not found')
            return redirect('forgot-password')
    
    return render(request, 'expenses/reset_password.html')

def success_password_reset(request):
    return render(request, 'expenses/success_password_reset.html')

def userHomePage(request):
    return render(request, 'expenses/user_home.html')

def add_user_expenses(request):
    categories = Category.objects.all()
    

    if request.method =="POST":
        title = request.POST.get('title')
        amount =  request.POST.get('amount')
        description = request.POST.get('description')   
        date = request.POST.get('date') 
        category_id=request.POST.get('category')

        category  = Category.objects.get(id=category_id)

        Expenses.objects.create(
            user=request.user,
            title=title,
            amount=amount,
            description=description,
            date=date,
            category=category
        )
        
        return redirect('user-total-expenses')

    context = {'categories': categories}
    return render(request, 'user_profile/add_user_expenses.html', context) 

def user_total_expenses(request):
    expenses = Expenses.objects.all()
    total_Expenses = sum(total.amount for total in expenses)

    context = {'expenses': expenses,
                'total_amount': total_Expenses}
    return render(request, 'user_profile/user_total_expenses.html', context )