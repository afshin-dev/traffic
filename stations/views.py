from django.shortcuts import render
from rest_framework.viewsets import  ViewSet , ModelViewSet
from rest_framework.request import Request 
from rest_framework.response import Response 
from .serializers import StationSerializer , StationCrossSerializer, TollPaymentSerializer
from .models import Station, StationCross, TollPayment
from rest_framework import status

class StationViewSet(ViewSet):

    def list(self, request: Request) -> Response:
        stations = Station.objects.all()
        ser = StationSerializer(stations, many=True)

        return Response(ser.data)

    def create(self, request: Request) -> Response:
        """
            sample data for create a station record 
            {
            "name" : "" ,
            "toll_per_cross" : 0 , 
            "location" : "long, lat"
            }
        """
        station_data = StationSerializer(data=request.data) 
        if not station_data.is_valid():
            return Response(station_data.errors, status=status.HTTP_400_BAD_REQUEST)
        
        new_station = station_data.save() 

        station_ser = StationSerializer(new_station)
        return Response(station_ser.data)

    def update(self, request:Request, pk=int):
        try:
            station = Station.objects.get(pk=pk)
            ser = StationSerializer(data=request.data, instance=station)
            if ser.is_valid():
                updated_station = ser.save()
                updated_station_deser = StationSerializer(updated_station)
                return Response(updated_station_deser.data, status=status.HTTP_202_ACCEPTED)
            else :
                return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)   
        except Station.DoesNotExist:
            return Response({"error": "not found"}, status=status.HTTP_404_NOT_FOUND)   
        except Exception:
            return Response({"error": "internal error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

    def retrieve(self, request: Request, pk:int):
        try:
            station = Station.objects.get(pk=pk)
            deser = StationSerializer(station)
            return Response(deser.data, status=status.HTTP_200_OK)
        
        except Station.DoesNotExist:
            return Response({"error": "not found"}, status=status.HTTP_404_NOT_FOUND)   
        
        except Exception:
            return Response({"error": "internal error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
        
    def delete(self, request: Request, pk:int):
        try:
            station = Station.objects.get(pk=pk)
            station.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        except Station.DoesNotExist:
            return Response({"error": "not found"}, status=status.HTTP_404_NOT_FOUND)   


class StationCrossModelViewSet(ModelViewSet):
    queryset = StationCross.objects.all()
    serializer_class = StationCrossSerializer





class TollPaymentViewSet(ViewSet):

    def create(self, request: Request) -> Response:
        toll_payment_ser = TollPaymentSerializer(data=request.data) 
        if not toll_payment_ser.is_valid():
            return Response(toll_payment_ser.errors, status=status.HTTP_400_BAD_REQUEST)
        
        paid_toll = toll_payment_ser.save() 

        paid_toll_ser = TollPaymentSerializer(paid_toll)
        return Response(paid_toll_ser.data)
    

