import django_filters
from django_filters import DateFilter
from fms.models import Received, Sent


class SentFilter(django_filters.FilterSet):    
    start_date = django_filters.DateFilter(field_name="date_created", lookup_expr='gte') 
    end_date = django_filters.DateFilter(field_name="date_created", lookup_expr='lte') 
     
    subject__icontains = django_filters.CharFilter(field_name="subject", lookup_expr='icontains')
    file_name__icontains = django_filters.CharFilter(field_name="file_name", lookup_expr='icontains')
    institution__icontains = django_filters.CharFilter(field_name="institution", lookup_expr='icontains')
    
    class Meta:
        model = Sent
        fields = '__all__'
        exclude = ['file',]     
        
 
       


class ReceivedFilter(django_filters.FilterSet):    
    start_date = django_filters.DateFilter(field_name="date_created", lookup_expr='gte') 
    end_date = django_filters.DateFilter(field_name="date_created", lookup_expr='lte') 
    subject__icontains = django_filters.CharFilter(field_name="subject", lookup_expr='icontains')
    file_name__icontains = django_filters.CharFilter(field_name="file_name", lookup_expr='icontains')
    institution__icontains = django_filters.CharFilter(field_name="institution", lookup_expr='icontains')
    date_received__icontains = django_filters.CharFilter(field_name="date_received", lookup_expr='icontains')
    class Meta:
        model = Received
        fields = '__all__'
        exclude = ['file',]        