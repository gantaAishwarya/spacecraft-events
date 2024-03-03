from django_filters import rest_framework as filters
from .models import Events,Longitude,Latitude

class EventsFilter(filters.FilterSet):
    event_name = filters.CharFilter(field_name='event_name')

    class Meta:
        model = Events
        fields = ['event_name']


class LongitudeFilter(filters.FilterSet):
    position = filters.NumberFilter(field_name='position')

    class Meta:
        model = Longitude
        fields = ['position',] 

class LatitudeFilter(filters.FilterSet):
    position = filters.NumberFilter(field_name='position')

    class Meta:
        model = Latitude
        fields = ['position',] 