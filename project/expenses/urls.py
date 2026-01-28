from django.urls import path
from .views import category_home, expenses_home, category_page, userSignup, userLogin, forgot_password, verify_otp, reset_password, success_password_reset, userLogout, userHomePage, add_user_expenses, user_total_expenses
urlpatterns = [
     path('', category_home, name='category-home'),
     path('expenses', expenses_home , name='expenses_home'),
     path('category/<int:pk>', category_page , name='category_page'),
     path('user-signup', userSignup, name='user-signup'),
     path('user-login', userLogin, name='user-login'),
     path('forgot-password/', forgot_password, name='forgot-password'),
     path('verify-otp/', verify_otp, name='verify-otp'),
     path('reset-password/', reset_password, name='reset-password'),
     path('success-password-reset/', success_password_reset, name='success-password-reset'),
     path('user-logout/', userLogout, name='user-logout'),
     path('user-home/', userHomePage, name='user-home'), 
     path('add-user-expenses/', add_user_expenses, name='add-user-expenses'),
     path('user-total-expenses/', user_total_expenses, name='user-total-expenses'),

 ]
