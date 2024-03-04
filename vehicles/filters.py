from django_filters import FilterSet 
import django_filters
from .models import VehicleOwner

class VehicleOwnerFilter(FilterSet):
    min_user_age = django_filters.NumberFilter(field_name='user__age', lookup_expr='gt')

    # class Meta:
    #     model = VehicleOwner
    #     fields = ['user']