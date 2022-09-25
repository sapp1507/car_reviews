from rest_framework import serializers

from reviews.models import Brand, Car, Comment, Country


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода и записи комментариев"""
    email = serializers.EmailField(required=False)
    pub_date = serializers.DateTimeField(format='%H:%m %d %B %Y',
                                         read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'email', 'car', 'pub_date', 'text']
        extra_kwargs = {
            'car': {'write_only': 'True'}
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if user.is_authenticated:
            return value
        if not value:
            raise serializers.ValidationError('Обязательное поле!')
        return value

    def create(self, validated_data):
        comment = Comment(**validated_data)
        author = self.context['request'].user
        if author.is_authenticated:
            comment.author = author
            comment.email = author.email
        comment.save()
        return comment


class CarSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода автомобиля"""
    brand = serializers.StringRelatedField()
    comments_count = serializers.SerializerMethodField(read_only=True)
    comments = CommentSerializer(read_only=True, many=True)

    class Meta:
        model = Car
        fields = ['id', 'url', 'name', 'brand', 'year_release',
                  'year_completion', 'comments_count', 'comments']

    def get_comments_count(self, car):
        return car.comments.count()


class AddCarSerializer(serializers.ModelSerializer):
    """Сериализатор для записи автомобиля"""
    year_completion = serializers.IntegerField(required=False)

    class Meta:
        model = Car
        fields = ['name', 'brand', 'year_release', 'year_completion']

    def to_representation(self, instance):
        serializer = CarSerializer(instance, context=self.context)
        return serializer.data

    def validate(self, attrs):
        car = Car(**attrs)
        if car.year_completion and car.year_release > car.year_completion:
            raise serializers.ValidationError(
                {'year_release': ('Год начала выпуска не может быть больше'
                                  'года завершения выпуска')}
            )
        return attrs


class CarForBrandSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода автомобиля в производителях"""
    comments_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'name', 'comments_count']

    def get_comments_count(self, car):
        return car.comments.count()


class BrandSerializer(serializers.ModelSerializer):
    """Сериализатор для вывода производителя"""
    country = serializers.StringRelatedField()
    cars = CarForBrandSerializer(read_only=True, many=True)

    class Meta:
        model = Brand
        fields = ['id', 'name', 'country', 'url', 'cars']


class AddBrandSerializer(serializers.ModelSerializer):
    """Сериализатор для записа производителя"""
    class Meta:
        model = Brand
        fields = ['name', 'country']

    def to_representation(self, instance):
        serializer = BrandSerializer(instance, context=self.context)
        return serializer.data


class BrandForCountrySerializer(serializers.ModelSerializer):
    """Сериализатор для вывода прозводитея в стране"""
    class Meta:
        model = Brand
        fields = ['id', 'name', 'url']


class CountrySerializer(serializers.ModelSerializer):
    """Сериализитор для вывода страны"""
    brands = BrandForCountrySerializer(read_only=True, many=True)

    class Meta:
        model = Country
        fields = ['id', 'url', 'name', 'brands']
