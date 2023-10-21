from django.contrib import admin
from . models import Received, Sent, Profile
# Register your models here.
admin.site.register(Received)
admin.site.register(Profile)
admin.site.register(Sent)
