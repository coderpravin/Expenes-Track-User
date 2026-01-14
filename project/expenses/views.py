from django.shortcuts import render
from .models import Category,Expenses
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