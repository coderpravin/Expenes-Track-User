from django.urls import path
from .views import category_home,user_signup, user_login
urlpatterns = [
     path('', category_home, name='category-home'),
     path('signup/', user_signup, name='user-signup'),
     path('login/', user_login, name='user-login'),
 ]