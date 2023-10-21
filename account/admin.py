from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from fms.models import Profile

class ProfileAdminForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ()

class CustomUserAdmin(UserAdmin):
    form = ProfileAdminForm

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
