from django.contrib.auth.mixins import LoginRequiredMixin

class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = '/'  # Customize the login URL if needed
