from django.urls import path 
from rest_framework.routers import DefaultRouter 
from .views import VehicleModelViewSet , VehicleTypeViewSet, OwnerModelViewSet

router = DefaultRouter() 

router.register(r'all', VehicleModelViewSet, basename='vehicle')
router.register(r'types', VehicleTypeViewSet, basename='vehicletype')
router.register(r'owners',OwnerModelViewSet , basename='owner')

urlpatterns = router.urls
