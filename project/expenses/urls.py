from django.urls import path
from .views import category_home,user_signup, user_login, forgot_password
urlpatterns = [
     path('', category_home, name='category-home'),
     path('signup/', user_signup, name='user-signup'),
     path('login/', user_login, name='user-login'), 
     path('forgot-password/', forgot_password, name='forgot-password'),
 ]