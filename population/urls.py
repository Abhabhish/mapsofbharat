from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='index'),
    path('api/population/', views.get_population, name='get_population'),

    path('get-districts/', views.get_districts, name='get_districts'),
    path('get-subdistricts/', views.get_sub_districts, name='get_sub_districts'),
    path('get-blocks/', views.get_blocks, name='get_blocks'),
    path('get-pincodes/', views.get_pincodes, name='get_pincodes'),
    path('get-gram_panchayats/', views.get_gram_panchayats, name='get_gram_panchayats'),
    path('get-town_villages/', views.get_town_villages, name='get_town_villages'),
    
    path('get-applicable_boundaries/', views.get_aplicable_boundaries, name='get_aplicable_boundaries'),

    path('add_color_family/',views.add_color_family,name='add_color_family'),
    path('add-color-range/', views.add_color_range, name='add_color_range'),

    path('get_color_families/',views.get_color_families,name="get_color_families"),
    path('get_color_ranges/<int:family_id>/',views.get_color_ranges,name='get_color_ranges'),

    path('delete-family/<int:pk>/', views.delete_color_family, name='delete_color_family'),
    path('delete-range/<int:pk>/', views.delete_color_range, name='delete_color_range'),

]


