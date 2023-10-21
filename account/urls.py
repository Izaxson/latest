from django.urls import path
from django.views import View
from account import auth_views
from account.auth_views import    SendOTPView, UserLoginView, VerifyOTPView

urlpatterns = [
#  path('otploginview', OTPLoginView.as_view(), name='otploginview'),  
 path('',UserLoginView.as_view(), name='login'),  
#  path('', auth_views.user_login, name='login'),
 path('logout/', auth_views.user_logout, name='logout'),

 path('send_otp/', SendOTPView.as_view(), name='send_otp'),
 path('verify_otp/', VerifyOTPView.as_view(), name='verify_otp'),
#   path('login/', auth_views.LoginView.as_view(), name='login'),
#   path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]