from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .api_router import CustomDefaultRouter
from spacecraft.views import Events_detail, LongitudeViewSet, LatitudeViewSet, Events_list


router = CustomDefaultRouter()
router.register("Longitude", LongitudeViewSet, basename="Longitude")
router.register("Latitude", LatitudeViewSet, basename="Latitude")


# Swagger documentation setup
schema_view = get_schema_view(
    openapi.Info(
        title="Solenix API",
        default_version='v1',
        description="Solenix Demo Documentation",
        terms_of_service="#",
        contact=openapi.Contact(email="contact@solenix.net"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/", include(router.urls)),
    path('api/events/', Events_list),
    path('api/events/<str:id>', Events_detail),
    re_path(r'^docs(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# URL pattern for serving static files collected during python manage.py collectstatic for efficient debugging
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "Solenix Super Admin"
admin.site.site_title = "Solenix"
admin.site.index_title = "Solenix Super Admin"