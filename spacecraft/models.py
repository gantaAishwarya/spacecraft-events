from django.db import models
from django.utils.translation import gettext_lazy as _
import re
from django.core.exceptions import ValidationError


class Events(models.Model):
    occurrence_time = models.DateTimeField(null=False, help_text=_("Date and time of the event occurance"))
    event_name= models.CharField(max_length=200,null=False, help_text=_("Name of the event"))
    id= models.CharField(primary_key=True,max_length=4,null=False, help_text=_("Event ID"), editable=False)
    severity= models.CharField(max_length=200,null=True, help_text=_("Severity of the event"))

    # def clean(self):
    #     # Validate the format of the event id
    #     id_pattern = re.compile(r'^E\d{3}$')
    #     if not id_pattern.match(self.id.strip()):
    #         raise ValidationError({"id": ["Event ID must be in the format 'E' followed by three digits (e.g., E001)."]})


    # def save(self, *args, **kwargs):
    #     self.full_clean() 
    #     super().save(*args, **kwargs)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.event_name 

class Longitude(models.Model):
    timestamp = models.DateTimeField(null=False, help_text=_("Time stamp of the recorded longitude position"))
    position = models.DecimalField(max_digits=9,null=False,decimal_places=4 ,help_text=_("Longitude position"))

class Latitude(models.Model):
    timestamp = models.DateTimeField(null=False, help_text=_("Time stamp of the recorded latitude position"))
    position = models.DecimalField(max_digits=9,null=False,decimal_places=4 ,help_text=_("Latitude position")) 
