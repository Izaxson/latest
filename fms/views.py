import math
import os
import random
from sqlite3 import DatabaseError
from django.http import FileResponse, Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.views import PasswordChangeView
import os
from django.conf import settings
from django.views.generic import CreateView,ListView,DetailView,FormView,UpdateView,DeleteView 
from django.contrib import messages
from django.contrib.auth.models import User
from account import forms
from core import settings
from fms.filter import ReceivedFilter, SentFilter
from fms.forms import  ReceivedForm, SentForm,UpdateReceivedForm,UpdateSentForm ,ProfilePictureForm
import mimetypes
from django.views.generic import TemplateView
from fms.mixins import CustomLoginRequiredMixin
from .models import Received, Sent  # Import the Received and Sent models
from django_filters.views import FilterView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from .models import *
import pandas as pd
from django.db.models import Count
from django.db.models.functions import TruncMonth
from .models import Received  # Import your Received model here
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


from django.contrib.auth.decorators import user_passes_test

def is_clerk(user):
    return user.groups.filter(name='is_clerk').exists()

def is_governor(user):
    return user.groups.filter(name='is_governor').exists()

def is_clerk_or_governor(user):
    return is_clerk(user) or is_governor(user)

# class ChartsView(CustomLoginRequiredMixin,View):
#     template_name = 'fms/charts.html'

#     def get(self, request):
#         # Query the database and group by month
#         items = Received.objects.annotate(month=TruncMonth('date_received')).values('month').annotate(count=Count('id'))

#         # Create a DataFrame from the queryset
#         df = pd.DataFrame(items)

#         # Convert the 'month' column to a datetime-like object (assuming 'date_field' is a date or datetime field)
#         df['month'] = pd.to_datetime(df['month'])

#         # Rename the columns for clarity
#         df = df.rename(columns={'month': 'Month', 'count': 'Received Count'})

#         # Convert the 'Month' column to a more readable format (e.g., 'YYYY-MM')
#         df['Month'] = df['Month'].dt.strftime('%Y-%m')

#         # Convert the DataFrame to lists
#         months = df['Month'].tolist()
#         received_count = df['Received Count'].tolist()

#         # Create a dictionary to pass to the template
#         context = {"months": months, 'received_count': received_count}

#         return render(request, self.template_name, context=context)



class DashboardView(CustomLoginRequiredMixin,TemplateView):
    template_name = 'fms/dashboard.html'
    login_url = '/'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        try:
            incoming_count = Received.objects.all().count()
            sent_count = Sent.objects.all().count()
            users_count = User.objects.all().count()
            # Calculate the total count
            total_count = incoming_count + sent_count
            percent_received=(math.floor( (incoming_count/total_count)*100))
            percent_sent=(math.floor( (sent_count/total_count)*100))
            context['received_count'] = incoming_count
            context['users_count'] = users_count
            context['sent_count'] = sent_count
            context['total_count'] = total_count  # Add the total count to the context
            context['percent_received'] = percent_received
            context['percent_sent'] = percent_sent
        except Exception as e:
            # Handle any exceptions gracefully
            context['incoming_count'] = "loading...."
            context['sent_count'] = "...."
            context['total_count'] = "...."
            context['users_count'] = "...."
        
        return context
    
    
# `class CustomPasswordChangeView(PasswordChangeView):
#     template_name = 'fms/profile.html'  
#     success_url = reverse_lazy('profile') ` # Redirect URL after successful password change

 
# class ProfileView(CustomLoginRequiredMixin,TemplateView):
#     template_name = 'fms/profile.html'
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
        
#         try:
#             received_count = Received.objects.all().count()
#             sent_count = Sent.objects.all().count()
#             users_count = User.objects.all().count()
#             # Calculate the total count
#             total_count = received_count + sent_count
#             percent_received=(math.floor( (received_count/total_count)*100))
#             percent_sent=(math.floor( (sent_count/total_count)*100))
#             context['received_count'] = received_count
#             context['users_count'] = users_count
#             context['sent_count'] = sent_count
#             context['total_count'] = total_count  # Add the total count to the context
#             context['percent_received'] = percent_received
#             context['percent_sent'] = percent_sent
#         except Exception as e:
#             # Handle any exceptions gracefully
#             context['received_count'] = "...."
#             context['sent_count'] = "...."
#             context['total_count'] = "...."
#             context['users_count'] = "...."
        
#         return context


clerk_required = user_passes_test(is_clerk, login_url='login')
class MySentView(CustomLoginRequiredMixin,FilterView):
    template_name = 'fms/outgoing/mysent.html'
    model = Sent
    context_object_name = 'sent'
    filterset_class = SentFilter
  
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(uploaded_by=self.request.user.profile)

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name=search_query) ,
                Q(subject__icontains=search_query)
            )

        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs   
clerk_required = user_passes_test(is_clerk, login_url='login')    
class MyCapturesView(CustomLoginRequiredMixin,FilterView):
    template_name = 'fms/incoming/mycaptures.html'
    model = Received
    context_object_name = 'received'
    filterset_class = ReceivedFilter
  
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(uploaded_by=self.request.user.profile)

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name=search_query) ,
                Q(subject__icontains=search_query)
            )

        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs    
clerk_required = user_passes_test(is_clerk, login_url='login')
class ReceivedListView(CustomLoginRequiredMixin,FilterView):
    template_name = 'fms/incoming/received.html'
    model = Received
    context_object_name = 'received'
    filterset_class = ReceivedFilter
  
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = queryset.filter(profile=self.request.user.profile)

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name=search_query) ,
                Q(subject__icontains=search_query)
            )

        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs
    #search Received
governor_required = user_passes_test(is_governor, login_url='login')
class SearchReceivedListView(CustomLoginRequiredMixin,FilterView):
    template_name = 'fms/incoming/search.html'
    model = Received
    context_object_name = 'search'
    filterset_class = ReceivedFilter
   
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = queryset.filter(profile=self.request.user.profile)

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name=search_query) ,
                Q(subject__icontains=search_query)
            )

        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs
clerk_required = user_passes_test(is_clerk, login_url='login')           
class ReceivedAddView(CustomLoginRequiredMixin,FormView):
    template_name = 'fms/incoming/addreceived.html'
    form_class = ReceivedForm
    success_url = reverse_lazy('received')
    
    def form_valid(self, form):
        uploaded_by = self.request.user.profile  # attaching user to captured  bby 
        form = form.save(commit=False)
        form.uploaded_by = uploaded_by
        form.save()
        

        messages.success(self.request, 'Your File has been saved. Thank you!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.warning(self.request, 'Only PDF Document can be uploaded.')
        return self.render_to_response(self.get_context_data(form=form))

clerk_required = user_passes_test(is_clerk, login_url='login')
class UpdateReceived(CustomLoginRequiredMixin,UpdateView):
    template_name = 'fms/incoming/editreceived.html'
    form_class = UpdateReceivedForm
    success_url = reverse_lazy('received')

    def form_valid(self, form):
        form.save()

        messages.success(self.request, 'Your File details has been updated. Thank you!')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        file_id = self.kwargs.get('file_id')
        return Received.objects.get(pk=file_id) 

class DeleteReceived(CustomLoginRequiredMixin,DeleteView):
    model = Received
    success_url = reverse_lazy('received')  # Redirect to the success URL after deletion

    def get_object(self, queryset=None):
        file_id = self.kwargs.get('file_id')
        return get_object_or_404(Received, id=file_id)


clerk_required = user_passes_test(is_clerk, login_url='login') 
class SentListView(CustomLoginRequiredMixin,FilterView):
    template_name = 'fms/outgoing/sent.html'
    model = Sent
    context_object_name = 'sent'
    filterset_class = SentFilter
 
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = queryset.filter(profile=self.request.user.profile)

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name=search_query) ,
                Q(Vehicle__icontains=search_query)
            )

        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs
    
governor_required = user_passes_test(is_governor, login_url='login')    
class SearchSentListView(CustomLoginRequiredMixin,FilterView):
    template_name = 'fms/outgoing/search.html'
    model = Sent
    context_object_name = 'search'
    filterset_class = SentFilter
  
    
    def get_queryset(self):
        queryset = super().get_queryset()
        # queryset = queryset.filter(profile=self.request.user.profile)

        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(name=search_query) ,
                Q(subject__icontains=search_query)
            )

        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        return self.filterset.qs



clerk_required = user_passes_test(is_clerk, login_url='login')
class SentAddView(CustomLoginRequiredMixin,FormView):
    template_name = 'fms/outgoing/addsent.html'
    form_class=SentForm
    success_url = reverse_lazy('sent')

    def form_valid(self, form):
        uploaded_by = self.request.user.profile  # attaching user to captured  bby 
        form = form.save(commit=False)
        form.uploaded_by = uploaded_by
        form.save()

        messages.warning(self.request, 'Your File has been saved. Thank you!')
        return super().form_valid(form)   
    
    def form_invalid(self, form):
        messages.warning(self.request, 'Only PDF Document can be uploaded.')
        return self.render_to_response(self.get_context_data(form=form))
    
clerk_required = user_passes_test(is_clerk, login_url='login')
class UpdateSent(CustomLoginRequiredMixin,UpdateView):
    template_name = 'fms/outgoing/editsent.html'
    form_class = UpdateSentForm
    success_url = reverse_lazy('sent')

    def form_valid(self, form):
        form.save()

        messages.success(self.request, 'Your File details has been updated. Thank you!')
        return super().form_valid(form)

    def get_object(self, queryset=None):
        file_id = self.kwargs.get('file_id')
        return Sent.objects.get(pk=file_id) 

class DeleteSent(CustomLoginRequiredMixin,DeleteView):
    model = Sent
    template_name = 'fms/outgoing/delete.html'
    success_url = reverse_lazy('sent')  # Redirect to the success URL after deletion

    def get_object(self, queryset=None):
        file_id = self.kwargs.get('file_id')
        return get_object_or_404(Sent, id=file_id)
    
class ReceivedDownloadFileView(CustomLoginRequiredMixin,View):
    def get(self, request, file_id):
        uploaded_file = Received.objects.get(pk=file_id)
        response = HttpResponse(
            uploaded_file.file, content_type='application/force-download'
        )
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
        return response
    
class SentDownloadFileView(CustomLoginRequiredMixin,View):
    def get(self, request, file_id):
        try:
            uploaded_file = Sent.objects.get(pk=file_id)
        except Sent.DoesNotExist:
            return HttpResponse("File not found", status=404)

        response = HttpResponse(
            uploaded_file.file.read(), content_type='application/force-download'
        )
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'

        return response


class SearchResultsView(CustomLoginRequiredMixin,FilterView):
    model = Received
    template_name = 'fms/incoming/search.html'  # Create this template
    filterset_class = ReceivedFilter
    context_object_name = 'search'
    paginate_by = 10  # Adjust as needed
    
    def get_queryset(self):
        form = ReceivedForm(self.request.GET)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            entity = form.cleaned_data.get('entity')
            institution = form.cleaned_data.get('institution')
            date_from = form.cleaned_data.get('date_from')
            date_to = form.cleaned_data.get('date_to')
            priority = form.cleaned_data.get('priority')
            
            queryset = Received.objects.all()
            
            # Apply filtering based on the form fields
            if subject:
                queryset = queryset.filter(subject__icontains=subject)
            if entity:
                queryset = queryset.filter(entity__icontains=entity)
            if institution:
                queryset = queryset.filter(institution__icontains=institution)
            if priority:
                queryset = queryset.filter(priority__icontains=priority)
            
            # Apply date range filtering if provided
            if date_from:
                queryset = queryset.filter(date_received__gte=date_from)
            if date_to:
                queryset = queryset.filter(date_received__lte=date_to)
            
            return queryset
        return Received.objects.none()
clerk_required = user_passes_test(is_clerk, login_url='login')  
class ReceivedViewFile(CustomLoginRequiredMixin,View):
    def get(self, request, file_id):
        try:
            uploaded_file = Received.objects.get(pk=file_id)
        except Received.DoesNotExist:
            return HttpResponse("File not found", status=404)

        # Determine the content type based on the file extension
        file_name = uploaded_file.file.name
        content_type = 'application/octet-stream'  # Default content type for unknown files

        if file_name.endswith('.pdf'):
            content_type = 'application/pdf'
  
        response = HttpResponse(uploaded_file.file.read(), content_type=content_type)

        # Remove the 'Content-Disposition' header to prevent a download prompt
        del response['Content-Disposition']

        return response    
    
clerk_required = user_passes_test(is_clerk, login_url='login')
class SentViewFile(CustomLoginRequiredMixin,View):
    def get(self, request, file_id):
        try:
            uploaded_file = Sent.objects.get(pk=file_id)
        except Sent.DoesNotExist:
            return HttpResponse("File  not found", status=404)

        # Determine the content type based on the file extension
        file_name = uploaded_file.file.name
        content_type = 'application/octet-stream'  # Default content type for unknown files

        if file_name.endswith('.pdf'):
            content_type = 'application/pdf'
        
        response = HttpResponse(uploaded_file.file.read(), content_type=content_type)

        # Remove the 'Content-Disposition' header to prevent a download prompt
        del response['Content-Disposition']

        return response   
   # password update
class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'fms/profile.html'
    success_url = reverse_lazy('dashboard')
    
    
    def form_valid(self, form):
        form.save()

        messages.success(self.request, 'Your Password has been updated')
        return super().form_valid(form)
    


class ProfilePictureUpdateView(UpdateView):
    model = Profile
    form_class = ProfilePictureForm  # 
    template_name = 'fms/profile.html'  # 
    success_url = reverse_lazy('dashboard')  # Redirect to the user's profile page

    def form_valid(self, form):
        messages.success(self.request, 'Profile picture updated successfully.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error updating profile picture. Please try again.')
        return super().form_invalid(form)    
    
class ProfileView(UpdateView):
    model = Profile
    
    template_name = 'fms/photoupdate.html'  # 