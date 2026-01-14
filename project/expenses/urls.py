from django.urls import path
from .views import category_home, expenses_home, category_page, userSignup, userLogin
urlpatterns = [
     path('', category_home, name='category-home'),
     path('expenses', expenses_home , name='expenses_home'),
     path('category', category_page , name='category_page'),
     path('user-signup', userSignup, name='user-signup'),
     path('user-login', userLogin, name='user-login'),
 ]