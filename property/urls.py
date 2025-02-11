from django.urls import path
from . import views

urlpatterns = [
    path('create-property/', views.create_property, name='create_property'),
    path('create-land-location/<int:property_id>/', views.create_land_location, name='create_land_location'),
]
