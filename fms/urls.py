from django.urls import path
from fms import views
urlpatterns = [


   #profile update change
   path('photoupdate/<int:pk>/', views.ProfileView.as_view(), name='photoupdate'),  # Adjust the view name as needed
   path('password_change/', views.CustomPasswordChangeView.as_view(), name='password_change'),
   # path('password_change_done/', 'password_change_done', name='password_change_done'),
   path('photoupdate/<int:pk>/', views.ProfilePictureUpdateView.as_view(), name='photoupdate'), 
   
   path('mycaptures', views.MyCapturesView.as_view(), name="mycaptures"),
   path('mysent', views.MySentView.as_view(), name="mysent"),
   path('home',views.DashboardView.as_view(),name='dashboard'),
   

# password change
   # path('password-change/' auth_views.PasswordChangeView.as_view(),name='password_change'),
   # path('password-change/done/',auth_views.PasswordChangeDoneView.as_view(),name='password_change_done'),
   
#RECEIVED URLS
   path('received',views.ReceivedListView.as_view(),name='received'),
   path('receivedsearch',views.SearchReceivedListView.as_view(),name='receivedsearch'),
   path('addreceived',views.ReceivedAddView.as_view(),name='addreceived'),
   path('edit-received/<int:file_id>',views.UpdateReceived.as_view(),name='edit-received'),
   path('delete-received/<int:file_id>',views.DeleteReceived.as_view(),name='delete-received'),
   path('view-file/<int:file_id>/', views.ReceivedViewFile.as_view(), name='view-file'),

   #Sent URLS
   path('sent',views.SentListView.as_view(),name='sent'),
   path('addsent',views.SentAddView.as_view(),name='addsent'),
   path('sentsearch',views.SearchSentListView.as_view(),name='sentsearch'),
   path('edit-sent/<int:file_id>',views.UpdateSent.as_view(),name='edit-sent'),
   path('delete-sent/<int:file_id>',views.DeleteSent.as_view(),name='delete-sent'),
   path('file/<int:file_id>/', views.SentViewFile.as_view(), name='file'),
#downloads
   path('download/<int:file_id>/', views.SentDownloadFileView.as_view(), name='sent_download_file'),
   path('received-download/<int:file_id>/', views.ReceivedDownloadFileView.as_view(), name='received-download'),

  
]