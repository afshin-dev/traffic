from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, UserLoginView
 

router  = DefaultRouter() 

router.register(r"users", UserViewSet, basename="user")


urlpatterns = router.urls + [path("login", UserLoginView.as_view(), name="accounts.login") ]
