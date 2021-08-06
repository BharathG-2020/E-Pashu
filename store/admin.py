from django import forms
from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (
    Animal,
    AnimalImage,
    AnimalSpecification,
    AnimalSpecificationValue,
    AnimalType,
    Category,
)

admin.site.register(Category, MPTTModelAdmin)


class AnimalSpecificationInline(admin.TabularInline):
    model = AnimalSpecification


@admin.register(AnimalType)
class AnimalTypeAdmin(admin.ModelAdmin):
    inlines = [
        AnimalSpecificationInline,
    ]


class AnimalImageInline(admin.TabularInline):
    model = AnimalImage


class AnimalSpecificationValueInline(admin.TabularInline):
    model = AnimalSpecificationValue


@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    inlines = [
        AnimalSpecificationValueInline,
        AnimalImageInline,
    ]
