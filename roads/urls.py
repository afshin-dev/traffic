from rest_framework.routers import DefaultRouter 
from .views import HeavyVehicleOnViewSet 


router = DefaultRouter()


router.register(r"", HeavyVehicleOnViewSet, basename='roads')



urlpatterns = router.urls 

# print(urlpatterns)
