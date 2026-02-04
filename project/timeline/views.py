from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ContactMessage

# Create your views here.
def home_expenses(request):
    return render(request, 'mainIndex/expense_home.html')

def contact_view(request):
    if request.method == "POST":
        ContactMessage.objects.create(
        name = request.POST.get('name'),
        email = request.POST.get('email'),
        mobile = request.POST.get('mobile'),
        message = request.POST.get('message'),
        )
        return redirect('contact')
    return render(request, 'mainIndex/contact.html')