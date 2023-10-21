import random
from urllib import request
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, login ,logout
from django.urls import reverse_lazy
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.conf import settings
from twilio.rest import Client
from django.core.mail import send_mail  # Import for sending emails

from account.forms import LoginForm
from fms.models import OTPVerification
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import LoginForm  # You need to import your LoginForm



# class OTPLoginView(View):
#     template_name = 'account/login.html'
#     redirect_authenticated_user = True  # Redirect logged-in users to the 'next' URL if provided

#     def get_success_url(self):
#         return reverse_lazy('dashboard')  # Customize the success URL as needed

#     def form_valid(self, form):
#         # Check if the user is verified with OTP
#         if self.request.user.is_authenticated and self.request.user.otpverification.is_verified:
#             return super().form_valid(form)
            
#         else:
#             return redirect('verify_otp')  # Redirect to the OTP verification view 
               
@method_decorator(login_required, name='dispatch')
class SendOTPView(View):
    def post(self, request, *args, **kwargs):
        user = request.user
        otp_token = str(random.randint(100000, 999999))  # Generate a random OTP

        # Check if the user already has an OTPVerification record, and update it if it exists.
        otp_verification, created = OTPVerification.objects.get_or_create(user=user)
        otp_verification.otp_token = otp_token
        otp_verification.save()
        print('otp_token')

        # # Send the OTP via email
        # send_mail(
        #     'Your OTP Code',
        #     f'Your OTP is: {otp_token}',
        #     'izaxson@gmail.com',  # Replace with your email settings
        #     [user.email],  # Send OTP to the user's email address
        #     fail_silently=False,
        # )

        return redirect('verify_otp')
class UserLoginView(View):
    template_name = 'account/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])

            if user is not None:
                if user.is_active:
                    login(request, user)
                    try:
                        otp_verification = OTPVerification.objects.filter(user=user).latest('created_at')
                        if otp_verification.is_verified:
                            return redirect('dashboard')
                        else:
                            messages.error(request, 'Error logging in to your account. Please confirm your credentials.')
                            return redirect('verify_otp')
                    except OTPVerification.DoesNotExist:
                        messages.error(request, 'No OTP verification associated with this user.')
                        return redirect('dashboard')
                else:
                    return HttpResponse('Disabled account')
            else:
                messages.error(request, 'Invalid user credentials.')
                return redirect('login')
        else:
            messages.error(request, 'Invalid form data. Please check your inputs.')
            return redirect('login')



def user_logout(request):
    logout(request)
    messages.error(request,'Session Terminated, Login again')
    return redirect('/')


      


@method_decorator(login_required, name='dispatch')
class VerifyOTPView(View):
    template_name = 'account/send_otp.html'

    def post(self, request, *args, **kwargs):
        otp_input = request.POST.get('otp_input')
        otp_verification = OTPVerification.objects.filter(user=request.user, is_verified=False).first()

        if otp_verification and otp_input == otp_verification.otp_token:
            otp_verification.is_verified = True
            otp_verification.save()

            # You can also send a confirmation email here if needed
            send_mail(
                'OTP Verified',
                'Your OTP has been successfully verified.',
                'izaxson@gmail.com',  # Replace with your email settings
                [request.user.email],  # Send confirmation to the user's email address
                fail_silently=False,
            )

            return redirect('dashboard')

        return render(request, self.template_name, {'error_message': 'Invalid OTP'})


        
