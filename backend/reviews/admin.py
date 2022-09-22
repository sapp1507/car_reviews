from django.contrib import admin

from .models import Brand, Car, Comment, Country


class CountryBrandInline(admin.TabularInline):
    model = Brand


class BrandCarModelInline(admin.TabularInline):
    model = Car


class CarCommentsInline(admin.TabularInline):
    model = Comment


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']
    inlines = [CountryBrandInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'country']
    search_fields = ['name', 'country']
    inlines = [BrandCarModelInline]


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'brand', 'year_release', 'year_completion']
    search_fields = ['name', 'brand']
    inlines = [CarCommentsInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['email', 'car', 'pub_date', 'text']

