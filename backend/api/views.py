from rest_framework import permissions, viewsets

from reviews.models import Brand, Car, Comment, Country

from .permissions import CommentsPermissions
from .serializers import (AddBrandSerializer, AddCarSerializer,
                          BrandSerializer, CarSerializer, CommentSerializer,
                          CountrySerializer)
from .utils import get_csv_or_xlsx


class BaseCustomModelViewSet(viewsets.ModelViewSet):
    """Базовая модель для проверки get параметра в запросе"""
    attr_to_export = ('id')

    def list(self, request, *args, **kwargs):
        if 'get' in request.GET:
            return get_csv_or_xlsx(self.queryset, self.attr_to_export,
                                   request.GET['get'])
        return super(BaseCustomModelViewSet, self).list(request, *args, **kwargs)


class CountryViewSet(BaseCustomModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    attr_to_export = ('id', 'name')


class BrandViewSet(BaseCustomModelViewSet):
    queryset = Brand.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    attr_to_export = ('id', 'name', 'country')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return BrandSerializer
        return AddBrandSerializer


class CarViewSet(BaseCustomModelViewSet):
    queryset = Car.objects.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    attr_to_export = ('id', 'name', 'brand', 'year_release', 'year_completion')

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return CarSerializer
        return AddCarSerializer


class CommentViewSet(BaseCustomModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (CommentsPermissions,)
    attr_to_export = ('id', 'author', 'email', 'pub_date', 'car', 'text')
