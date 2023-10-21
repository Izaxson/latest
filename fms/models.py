from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from PIL import Image

class OTPVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_token = models.PositiveIntegerField()
    is_verified = models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True) 
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')   
    phone_number = models.CharField(max_length=15, unique=True)  
    profile_pic = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpeg', 'jpg', 'gif', 'png'])]
        
    ) 
          
    @property
    def get_photo_url(self):
        if self.profile_pic and hasattr(self.profile_pic, 'url'):
            return self.profile_pic.url
        else:
            return "/static/images/logo.png"
        
    def __str__(self):
        return f'{self.user.username} '
    
    
    def save(self, *args, **kwargs):
        # save the profile first
        super().save(*args, **kwargs)

        # resize the image
        img = Image.open(self.profile_pic.path)
        if img.height > 400 or img.width > 400:
            output_size = (400, 400)
            # create a thumbnail
            img.thumbnail(output_size)    
            # overwrite the larger image
    
            img.save(self.profile_pic.path)
    


class Received(models.Model):
    OFFICE_TO = (
        ('Office of The Governor', 'Office of The Governor'),
        ('Office of The Deputy Governor', 'Office of The Deputy Governor')
    )

    Government = (
        ('Internal', 'Internal'),
        ('External', 'External'),
       
    )
   


  
    subject = models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    entity = models.CharField(choices=Government, max_length=100)  # 
    institution = models.CharField(max_length=100)
    date_received = models.DateField(blank=True,null=True)
    office_to = models.CharField(choices=OFFICE_TO, max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='files/Received/%Y/%m/%d/', validators=[FileExtensionValidator(['pdf'])])
    remarks = models.TextField(max_length=100, null=True, blank=True)
    uploaded_by = models.ForeignKey(Profile, on_delete=models.PROTECT)
    class Meta:
        ordering = ['-date_received']
        verbose_name = 'Received'
        verbose_name_plural = 'Received'

    def __str__(self):
        return self.subject

    
class Sent(models.Model):
   
    OFFICE_FROM = (
        ('Office of The Governor', 'Office of The Governor'),
        ('Office_of_The_Deputy_Governor', 'Office of The Deputy Governor')
    )

    Government = (
        ('Internal', 'Internal'),
        ('External', 'External'),
       
    )

   
    subject=models.CharField(max_length=100)
    file_name = models.CharField(max_length=100)
    sent_to=models.CharField(choices=Government,max_length=150)
    institution = models.CharField(max_length=100)
    date_sent = models.DateField()
    office_from= models.CharField(choices=OFFICE_FROM, max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='files/Sent/%Y/%m/%d/', validators=[FileExtensionValidator(['pdf'])])
    remarks = models.TextField(max_length=100,null=True,blank=True)
    uploaded_by = models.ForeignKey(Profile, on_delete=models.PROTECT)

    class Meta:
        ordering=['-date_sent']
        verbose_name = 'Sent'
        verbose_name_plural = 'Sent'
        
    
    def __str__(self):
        return self.subject