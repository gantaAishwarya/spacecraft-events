from django.contrib import admin
from .models import Events,Latitude,Longitude

#show models in django admin panel
class Admin(admin.ModelAdmin):
    search_fields = ["event_name"]
    list_display = ["event_name"]

admin.site.register(Events)
admin.site.register(Latitude)
admin.site.register(Longitude)