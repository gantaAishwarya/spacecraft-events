import json
import os
from django.core.management.base import BaseCommand
from spacecraft.models import Events,Latitude,Longitude


#To load data from json files to postgres db execute docker exec -it web python manage.py import_data
#This command is used for loaidng data from json files into the postgres db
class Command(BaseCommand):
    help = 'Import data from JSON files'

    def handle(self, *args, **options):
        json_files = ['events.json', 'latitudes.json', 'longitudes.json']

        for file_name in json_files:
            file_path = os.path.join('spacecraft', 'data',file_name)
            with open(file_path, 'r') as file:
                data = json.load(file)
                for entry in data:
                    if file_name == 'events.json':
                        Events.objects.create(**entry)
                    elif file_name == 'latitudes.json':
                        Latitude.objects.create(**entry)
                    elif file_name == 'longitudes.json':
                        Longitude.objects.create(**entry)

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
