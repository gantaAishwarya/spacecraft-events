from rest_framework import serializers
from .models import Events,Latitude,Longitude
from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder

class EventsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Events
        #instructs the serializer to include all fields
        fields = "__all__"
        #id field should be treated as read-only during serialization/deserialization
        read_only_fields = ["id"]


class LatitudeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Latitude
        #instructs the serializer to include all fields
        fields = "__all__"


class LongitudeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Longitude
        #instructs the serializer to include all fields
        fields = "__all__"

