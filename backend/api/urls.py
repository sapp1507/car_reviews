from django.urls import include, path, re_path
from rest_framework.routers import DefaultRouter

from .views import BrandViewSet, CarViewSet, CommentViewSet, CountryViewSet

router = DefaultRouter()
router.register(r'countrys', CountryViewSet, basename='country')
router.register(r'brands', BrandViewSet, basename='brand')
router.register(r'cars', CarViewSet, basename='car')
router.register(
    r'cars/(?P<car_id>\d+)/comments',
    CommentViewSet,
    basename='comment'
)


urlpatterns = [
    path('', include('djoser.urls')),
    path('', include(router.urls)),
    re_path(r'^auth/', include('djoser.urls.authtoken'))
]
