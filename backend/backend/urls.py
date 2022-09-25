from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('doc/', TemplateView.as_view(
        template_name='docs/redoc.html',
    ), name='redoc'),
    path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
]
