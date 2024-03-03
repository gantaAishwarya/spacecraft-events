from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
# from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticated
# from rest_framework.authentication import TokenAuthentication
from .models import Events,Latitude,Longitude
from .serializers import EventsSerializer, LongitudeSerializer, LatitudeSerializer
from django.http import JsonResponse
from .filters import EventsFilter, LatitudeFilter, LongitudeFilter
# from rest_framework.authtoken.views import ObtainAuthToken
# from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from datetime import datetime
# from rest_framework import generics

#If token authentication is required use code below
# class CustomAuthTokenLogin(ObtainAuthToken):
    
#     #Method that returns token if given user and password are valid
#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data,
#                                            context={'request': request})
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         token, created = Token.objects.get_or_create(user=user)
#         return Response({
#             'token': token.key,
#             #'user_id': user.pk,
#             'email': user.username
#         })


#Implemented POST api call to add new events if required
@api_view(['GET','POST'])
def Events_list(request, format=None):
    # Check if the request method is GET
    if request.method == 'GET':
        # Query all database rows for Events
        queryset = Events.objects.all()
        filterset_class = EventsFilter
        # Apply filters based on request.GET parameters
        filtered_queryset = filterset_class(request.GET, queryset=queryset).qs

        paginator = PageNumberPagination()
        # Update the query set according to the set paginator page value
        result_page = paginator.paginate_queryset(filtered_queryset, request)
        
        # Convert queryset to a data dictionary using the EventsSerializer
        serializer = EventsSerializer(result_page, many=True)

        for event_data in serializer.data:
            # Retrieve Latitude and Longitude positions for each event
            event_instance = Events.objects.get(pk=event_data['id'])
            latitude_position = Latitude.objects.filter(timestamp__lte=event_instance.occurrence_time).order_by('-timestamp').first()
            longitude_position = Longitude.objects.filter(timestamp__lte=event_instance.occurrence_time).order_by('-timestamp').first()

            # Serialize Latitude position
            nearest_latitude = (
                LatitudeSerializer(latitude_position).data.get('position') 
                if latitude_position else None
            )

            # Serialize Longitude position
            nearest_longitude = (
                LongitudeSerializer(longitude_position).data.get('position') 
                if longitude_position else None
            )

            # Add Latitude and Longitude information to the event_data
            event_data['nearest_latitude'] = nearest_latitude
            event_data['nearest_longitude'] = nearest_longitude

        # Return paginated response with the updated event data
        return paginator.get_paginated_response(serializer.data)
    
    #Use this below code if you want to add new event data 
    # if request.method == 'POST':
    #     serializer = EventsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         #If serializer is true then save the value in database
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     #If serializer fails then return error bad request
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE'])
def Events_detail(request, id, format=None):
    try:
        # Retrieve the Event instance by ID
        event_instance = Events.objects.get(pk=id)
    except Events.DoesNotExist:
        # If the specified ID doesn't exist, return a 404 Not Found response
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        # Retrieve the nearest longitude and latitude positions
        nearest_longitude_lte = Longitude.objects.filter(timestamp__lte=event_instance.occurrence_time).order_by('-timestamp').first()
        nearest_latitude_lte = Latitude.objects.filter(timestamp__lte=event_instance.occurrence_time).order_by('-timestamp').first()

        nearest_longitude_gte = Longitude.objects.filter(timestamp__gte=event_instance.occurrence_time).order_by('timestamp').first()
        nearest_latitude_gte = Latitude.objects.filter(timestamp__gte=event_instance.occurrence_time).order_by('timestamp').first()

        if nearest_longitude_lte and nearest_latitude_lte and nearest_longitude_gte and nearest_latitude_gte:
            # Serialize the longitude and latitude positions
            longitude_lte_serializer = LongitudeSerializer(nearest_longitude_lte)
            latitude_lte_serializer = LatitudeSerializer(nearest_latitude_lte)

            longitude_gte_serializer = LongitudeSerializer(nearest_longitude_gte)
            latitude_gte_serializer = LatitudeSerializer(nearest_latitude_gte)

            # Calculate time differences
            nearest_longitude_lte_datetime = datetime.fromisoformat(longitude_lte_serializer.data.get("timestamp"))
            timediff_long_lte = event_instance.occurrence_time - nearest_longitude_lte_datetime

            nearest_latitude_lte_datetime = datetime.fromisoformat(latitude_lte_serializer.data.get("timestamp"))
            timediff_lat_lte = event_instance.occurrence_time - nearest_latitude_lte_datetime

            nearest_longitude_gte_datetime = datetime.fromisoformat(longitude_gte_serializer.data.get("timestamp"))
            timediff_long_gte = nearest_longitude_gte_datetime - event_instance.occurrence_time

            nearest_latitude_gte_datetime = datetime.fromisoformat(latitude_gte_serializer.data.get("timestamp"))
            timediff_lat_gte = nearest_latitude_gte_datetime - event_instance.occurrence_time

            # Get positions based on time difference
            long_position = longitude_lte_serializer.data.get("position") if timediff_long_lte <= timediff_long_gte else longitude_gte_serializer.data.get("position")
            lat_position = latitude_lte_serializer.data.get("position") if timediff_lat_lte <= timediff_lat_gte else latitude_gte_serializer.data.get("position")

            # Construct the response in the format (longitude, latitude)
            res = f'(LONGITUDE: {long_position}, LATITUDE: {lat_position})'
            
        elif nearest_longitude_lte and nearest_latitude_lte and not nearest_longitude_gte and not nearest_latitude_gte:
            res = f'(LONGITUDE: {nearest_longitude_lte.position}, LATITUDE: {nearest_latitude_lte.position})'
        elif not nearest_longitude_lte and not nearest_latitude_lte and nearest_longitude_gte and nearest_latitude_gte:
            res = f'(LONGITUDE: {nearest_longitude_gte.position}, LATITUDE: {nearest_latitude_gte.position})'
        else:
            res = None

        # Return the response with the constructed data or None
        return Response(res, status=status.HTTP_200_OK)
 
    #Use this code below if you want to update existing event data
    # elif request.method == 'PUT':
    #     #convert the queryset to data dictionary using serializer
    #     serializer = EventsSerializer(Events, data=request.data)
    #     if serializer.is_valid():
    #         #If serializer is valid , save the data in database
    #         serializer.save()
    #         #sending updated data as response
    #         return Response(serializer.data,status=status.HTTP_200_OK)
    #     else:
    #         #If serializer is in valid then send bad request as status along with error
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    #Use this code if you want to delete existing data
    # elif request.method == 'DELETE':
    #     #Deleting the retrieved Events
    #     Events.delete()
    #     #sending error code 204 no content as response status
    #     return Response(status=status.HTTP_204_NO_CONTENT)
         

class LongitudeViewSet(ModelViewSet):
    model = Longitude
    serializer_class = LongitudeSerializer
    #permission_classes = [AllowAny]
    queryset = Longitude.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = LongitudeFilter 
    

class LatitudeViewSet(ModelViewSet):
    model = Latitude
    serializer_class = LatitudeSerializer
    #permission_classes = [AllowAny]
    queryset = Latitude.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = LatitudeFilter  