from datetime import date
# from profile import Profile
from fms.models import Received,Sent,Profile
from .import forms
from django.forms import ModelForm


from django import forms
    
class ReceivedForm(forms.ModelForm):
    class Meta:
        model = Received
        fields = ['subject', 'file_name', 'entity', 'institution', 'date_received', 'office_to', 'file', 'remarks']
        widgets = {
            'date_created': forms.DateInput(attrs={'type': 'date', 'max': date.today().strftime('%Y-%m-%d')}),
        }
      

class UpdateReceivedForm(forms.ModelForm):
    class Meta:
        model = Received
        fields = ['subject', 'file_name', 'entity', 'institution','date_received', 'office_to','file', 'remarks']

    # Define widgets for each field
    widgets = {
        'subject': forms.TextInput(attrs={'class': 'form-control'}),
        'file_name': forms.TextInput(attrs={'class': 'form-control'}),
        'entity': forms.TextInput(attrs={'class': 'form-control'}),
        'institution': forms.TextInput(attrs={'class': 'form-control'}),
       'date_received': forms.DateInput(attrs={'class': 'colsm=5' 'form-control',}),
        'office_to': forms.TextInput(attrs={'class': 'form-control'}),
        'file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),  # ClearableFileInput for file fields
        'remarks': forms.Textarea(attrs={'class': 'form-control'}),
    }

class SentForm(forms.ModelForm):
    class Meta:
        model = Sent
        fields=['subject','file_name','sent_to','institution','date_sent','office_from','file','remarks']        
        
class UpdateSentForm(forms.ModelForm):
    class Meta:
        model = Sent
        fields = ['subject', 'file_name', 'sent_to', 'institution', 'date_sent', 'office_from', 'file', 'remarks']
        
    # widgets = {
    #     'subject': forms.TextInput(attrs={'class': 'form-control'}),
    #     'file_name': forms.TextInput(attrs={'class': 'form-control'}),
    #     'sent_to': forms.TextInput(attrs={'class': 'form-control'}),
    #     'institution': forms.TextInput(attrs={'class': 'form-control'}),
    #     'date_sent': forms.DateInput(attrs={'class':'colsm=5' 'form-control',}),
    #     'office_from': forms.TextInput(attrs={'class': 'form-control'}),
    #     'file': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),  # ClearableFileInput for file fields
    #     'remarks': forms.Textarea(attrs={'class': 'form-control'}),
    # }
        

        
        
class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_pic']       