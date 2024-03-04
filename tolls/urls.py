from django.urls import path 
from . import views

urlpatterns = [
    path('vehicle_near_station/<int:toll_station_id>/', views.vehicle_near_toll_station, name="tolls.vehicle_toll"),
    path('user/<int:user_id>/',views.user_tolls, name="tolls.users")
]
