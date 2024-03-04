from django.shortcuts import render
from .models import Vehicle , VehicleType, VehicleOwner
from .serializers import VehicleSerializer, VehicleTypeSerializer, VehicleOwnerSerializer
from rest_framework.viewsets import ModelViewSet 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from typing import Any
from rest_framework.decorators import action 
from rest_framework.request import Request
from rest_framework.response import Response 
from stations.models import StationCross 
from stations.serializers import StationCrossSerializer
from rest_framework import status
from django_filters import rest_framework as filters
from .filters import VehicleOwnerFilter

class VehicleTypeViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    serializer_class = VehicleTypeSerializer
    def get_queryset(self):
        return VehicleType.objects.all()
    

class VehicleModelViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ('color',)

    serializer_class = VehicleSerializer
    def get_queryset(self):
        return Vehicle.objects.all()

    @action(detail=True, methods=['GET'])
    def get_tolls(self, request:Request, pk:int) -> Response:
        try:
            pk = int(pk)
        except:
            return Response({'errors': 'vehicle id invalide'}, status=status.HTTP_400_BAD_REQUEST)
        
        station_cross = StationCross.objects.filter(vehicle=pk, paid=False)      
        station_cross_ser = StationCrossSerializer(station_cross, many=True)
        return Response(station_cross_ser.data)




class OwnerModelViewSet(ModelViewSet):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated,IsAdminUser]
    serializer_class = VehicleOwnerSerializer

    filter_backends = (filters.DjangoFilterBackend,)
    # filterset_fields = ('user__age',)
    filterset_class = VehicleOwnerFilter

    def get_permissions(self):
        if self.action == "list":
            permision_classes = [IsAuthenticated]
        else:
            permision_classes = [IsAdminUser]
        return [permision() for permision in permision_classes]
    
    queryset = VehicleOwner.objects.all() 
    def get_queryset(self):
        if not self.request.user.is_staff:
            return VehicleOwner.objects.filter(user__id=self.request.user.id) 
        else:
            return VehicleOwner.objects.all() 
            

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['user'] = self.request.user 
        return ctx