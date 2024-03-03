from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone
from spacecraft.models import Events, Latitude, Longitude
from datetime import datetime, timedelta
from rest_framework import status

class EventsTestCase(TestCase):
    def test_create_event(self):
        # Create an event instance
        event = Events.objects.create(
            occurrence_time=timezone.now(),
            event_name="Test Event",
            id="E001",
            severity="Info"
        )
        # Retrieve the event from the database
        stored_event = Events.objects.get(id="E001")
        self.assertEqual(event, stored_event)

    def test_null_name_fails(self):
        with self.assertRaises(ValidationError):
            Events.objects.create(occurrence_time=timezone.now(), event_name=None, id="E002")

    def test_blank_severity(self):
        # Create an event without specifying 'severity', should default to None
        event = Events.objects.create(
            occurrence_time=timezone.now(),
            event_name="Event Without Severity",
            id="E003"
        )
        self.assertIsNone(event.severity)

    def test_create_latitude_longitude(self):
        # Create latitude and longitude instances
        latitude = Latitude.objects.create(timestamp=timezone.now(), position=35.1234)
        longitude = Longitude.objects.create(timestamp=timezone.now(), position=138.5678)

        # Retrieve the latitude and longitude from the database
        stored_latitude = Latitude.objects.get(position=35.1234)
        stored_longitude = Longitude.objects.get(position=138.5678)

        self.assertEqual(latitude, stored_latitude)
        self.assertEqual(longitude, stored_longitude)
    

    def test_get_latitude_longitude_for_event_id(self):
        # Create an event instance
        event = Events.objects.create(
            occurrence_time=datetime.now(),
            event_name="Test Event",
            id="E001",
            severity="Info"
        )
        # Create latitude and longitude instances associated with the event
        latitude = Latitude.objects.create(timestamp=datetime.now(), position=35.1234)
        longitude = Longitude.objects.create(timestamp=datetime.now(), position=138.5678)
        event.latitude = latitude
        event.longitude = longitude
        event.save()

        # Perform a GET request to retrieve latitude/longitude for the given event-id
        response = self.client.get(f'/api/events/{event.id}/')

        # Check if the response is successful (status code 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data contains latitude and longitude information
        self.assertIn('latitude', response.data)
        self.assertIn('longitude', response.data)
        self.assertEqual(response.data['latitude'], str(latitude.position))
        self.assertEqual(response.data['longitude'], str(longitude.position))

    def test_get_whole_list_of_events_and_positions(self):
        # Create multiple event instances
        for i in range(1, 4):
            event = Events.objects.create(
                occurrence_time=datetime.now() - timedelta(days=i),
                event_name=f"Test Event {i}",
                id=f"E00{i}",
                severity="Info"
            )
            # Create latitude and longitude instances associated with each event
            Latitude.objects.create(timestamp=datetime.now(), position=35.1234 + i)
            Longitude.objects.create(timestamp=datetime.now(), position=138.5678 - i)

        # Perform a GET request to retrieve the whole list of events and associated positions
        response = self.client.get('/api/events/')

        # Check if the response is successful (status code 200)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data contains a list of events
        self.assertIn('results', response.data)

        # Check if the first event in the list has associated latitude and longitude
        first_event = response.data['results'][0]
        self.assertIn('latitude', first_event)
        self.assertIn('longitude', first_event)
