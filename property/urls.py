from django.urls import path
from . import views

urlpatterns = [
    path('create-land-location/<int:property_id>/', views.create_land_location, name='create_land_location'),

    # New URLs for updates
    path('update-land-location/<int:property_id>/', views.update_land_location, name='update_land_location'),
]
