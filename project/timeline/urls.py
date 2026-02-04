from django.urls import path
from .import views

urlpatterns = [
     path('', views.home_expenses, name='home-expenses'),
     path('contact/', views.contact_view, name='contact'),

]
