import rest_framework.permissions
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('doc/', TemplateView.as_view(
        template_name='docs/redoc.html',
    ), name='redoc'),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('openapi/', get_schema_view(
            title="Your Project",
            description="API for all things …",
            version="1.0.0",
            permission_classes=[rest_framework.permissions.AllowAny]
        ), name='openapi-schema'),
]
