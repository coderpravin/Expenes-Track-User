import datetime
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
from timeline.models import Months, Year
from django.core.paginator import Paginator
from xhtml2pdf import pisa
from django.template.loader import get_template
from openpyxl import Workbook
from .tasks import send_register_email
from django.utils import timezone
from datetime import timedelta, date
from django.db.models import Sum
# Create your views here.

def category_home(request):
    catogories = Category.objects.all()
    context = {'categories': catogories}
    return render(request, 'expenses/category_home.html', context)

def category_page(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    context = {'category': category}
    return render(request, 'expenses/category_page.html', context)


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

            #Trigger here ceklery
            send_register_email.delay(user.email)
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
    expenses = Expenses.objects.filter(user=request.user)
    #last month calculation
    today = timezone.now().date()
    first_day_of_this_month= today.replace(day=1)
    last_day_of_last_month = first_day_of_this_month - timedelta(days=1)
    first_day_of_last_month= last_day_of_last_month.replace(day=1)

    total_last_month = expenses.filter(date__range=(first_day_of_last_month, last_day_of_last_month)).aggregate(total=Sum('amount'))['total'] or 0

    #Three month calculation
    def month_total(year, month):
        return expenses.filter(
            date__year=year,
            date__month=month
        ).aggregate(total=Sum('amount'))['total'] or 0

    # Current month
    feb_total = month_total(today.year, today.month)

    # Last month (Jan)
    jan_date = (today.replace(day=1) - timedelta(days=1))
    jan_total = month_total(jan_date.year, jan_date.month)

    # Two months back (Dec)
    dec_date = (jan_date.replace(day=1) - timedelta(days=1))
    dec_total = month_total(dec_date.year, dec_date.month)

    # Max value for progress bar scaling
    max_amount = max(feb_total, jan_total, dec_total, 1)

    context = {
        'total_last_month' : total_last_month,
        'feb_total': feb_total,
        'jan_total': jan_total,
        'dec_total': dec_total,
        'feb_percent': (feb_total / max_amount) * 100,
        'jan_percent': (jan_total / max_amount) * 100,
        'dec_percent': (dec_total / max_amount) * 100,
    }
    return render(request, 'expenses/user_home.html', context)

def add_user_expenses(request):
    categories = Category.objects.all()
    

    if request.method =="POST":
        title = request.POST.get('title')
        amount =  request.POST.get('amount')
        description = request.POST.get('description')   
        date = request.POST.get('date') 
        category_id=request.POST.get('category')

        try:
            date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, 'Invalid date format. Please use YYYY-MM-DD.')
            return redirect('add-user-expenses')

        #check year is 2025-2026
        date_year = date.year
        year_obj = Year(year=date_year)
        try:
            year_obj.clean()
        except Exception as e:
            messages.error(request, str(e))
            return redirect('add-user-expenses')

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
    months = Months.objects.all()
    last_year = Year.objects.last()
    first_year = Year.objects.first()
    expenses = Expenses.objects.filter(user=request.user)
    total_Expenses = sum(total.amount for total in expenses)

    
    #Find last Month

    
    context = {'expenses': expenses,
                'total_amount': total_Expenses,
                'months': months, 
                'last_year': last_year, 
                'first_year': first_year,
                
                }
    

    return render(request, 'user_profile/user_total_expenses.html', context )



def month_year_expenses(request):
    month_name = request.GET.get('month')
    year = request.GET.get('year')

    expenses = Expenses.objects.all()

    if month_name and year:
        try:
            month_number = datetime.datetime.strptime(month_name, '%B').month
            year = int(year)

            # Filter expenses by month and year
            expenses = expenses.filter(date__year=year, date__month=month_number)
        
        except ValueError:
            pass
    
    # Pagination: 10 records per page
    paginator = Paginator(expenses, 10)
    page_number = request.GET.get('page') #current page
    expenses = paginator.get_page(page_number) #current_ object
    context = {'month': month_name, 'year':year, 
               'expenses':expenses, 'page_obj':expenses}
    return render(request, 'user_profile/month_year_expenses.html',context)

def download_pdf(request):
    month_name = request.GET.get('month')
    year = request.GET.get('year')

    expenses = Expenses.objects.all()

    if month_name and year:
        month_number = datetime.datetime.strptime(month_name, '%B').month
        year = int(year)
        expenses = expenses.filter(date__year=year, date__month=month_number)
    
    template_path = 'user_profile/pdf_template.html'  # this PSF HTML page

    context = {
        'expenses': expenses,
        'month': month_name,
        'year': year,
        'total_amount': sum(e.amount for e in expenses),
    }
    #create pdf page 
    response = HttpResponse(content_type = 'application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Expenses_{month_name}_{year}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.pisaDocument(src=html, dest=response)
    if pisa_status.err:
        return HttpResponse('Error generating PDF <pre>' + html + '</pre>')
    return response
    

def download_excel(request):
    month_name = request.GET.get('month')
    year = request.GET.get('year')

    expenses = Expenses.objects.all()
    if month_name and year:
        month_number = datetime.datetime.strptime(month_name, '%B').month
        year = int(year)
        expenses = expenses.filter(date__year=year, date__month=month_number)
    
    #create Excel Book
    wb = Workbook()
    ws = wb.active
    ws.title = f"{month_name} {year} Expenses"

    #Create header row
    headers = ['#', 'Title', 'Category', 'Amount', 'Date', 'Description']
    ws.append(headers)

    #Write Expense valuye in row
    for i, expense in enumerate(expenses, start=1):
        ws.append([
            i, 
            expense.title,
            expense.category.name,
            expense.amount,
            expense.date.strftime("%Y-%m-%d"),
            expense.description
        ])
    total_amount = sum(e.amount for e in expenses)
    ws.append(['', '', 'Total', total_amount, '', ''])

    #Prepare HTTP response
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename=Expenses_{month_name}_{year}.xlsx'

    #save response in Excel
    wb.save(response)
    return response
