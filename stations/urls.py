from rest_framework.routers import DefaultRouter 
from .views import StationViewSet, StationCrossModelViewSet, TollPaymentViewSet

router = DefaultRouter() 

router.register(r'all', StationViewSet, basename='all')
router.register(r'cross', StationCrossModelViewSet, basename='station')
router.register(r'toll_payment', TollPaymentViewSet, basename='toll_payment')


urlpatterns = router.urls
