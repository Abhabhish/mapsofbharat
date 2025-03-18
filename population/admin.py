from django.contrib import admin
from .models import Population,Csv,Geojson,ColorRange,ColorRangeFamily


@admin.register(Population)
class PopulationAdmin(admin.ModelAdmin):
    list_display = ('state', 'district','sub_district','block','town_village','pincode','gram_panchayat', 'population', 'csv')

@admin.register(Csv)
class CsvAdmin(admin.ModelAdmin):
    list_display = ('csv_file', 'upload_date')

@admin.register(Geojson)
class GeojsonAdmin(admin.ModelAdmin):
    list_display = ('state_name',
                    'state_geojson',
                    'district_geojson',
                    'sub_district_geojson',
                    'block_geojson',
                    'town_village_geojson',
                    'pincode_geojson',
                    'gram_panchayat_geojson')


@admin.register(ColorRangeFamily)
class ColorRangeFamilyAdmin(admin.ModelAdmin):
    list_display = ('family_name', 'created_by')


@admin.register(ColorRange)
class ColorRangeAdmin(admin.ModelAdmin):
    list_display = ('start', 'end','color','color_range_family')