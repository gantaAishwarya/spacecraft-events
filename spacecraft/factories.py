import factory
from factory import Faker
from spacecraft.models import Latitude,Longitude,Events

class EventsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Events
    
    event_name = Faker('event_name')


class LatitudeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Latitude
    
    position = Faker('position')

class LongitudeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Longitude
    
    position = Faker('position')
