from django.shortcuts import render
from .models import Category
# Create your views here.

def category_home(request):
    catogories = Category.objects.all()
    context = {'categories': catogories}
    return render(request, 'expenses/category_home.html', context)
