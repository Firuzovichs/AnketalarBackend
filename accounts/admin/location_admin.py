from django.contrib import admin
from accounts.models import Region, District

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "order")
    search_fields = ("name",)
    ordering = ("order", "name")

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "region", "order")
    list_filter = ("region",)
    search_fields = ("name", "region__name")
    ordering = ("region__order", "order", "name")
    autocomplete_fields = ("region",)
