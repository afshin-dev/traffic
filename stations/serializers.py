from rest_framework.serializers import ModelSerializer , ValidationError 
from .models import Station, StationCross , TollPayment
from django.db  import transaction 
from vehicles.models import VehicleOwner
from accounts.models import User

from .utils import create_point


class StationSerializer(ModelSerializer):
    MIN_LONG = -180 
    MAX_LONG = 180 

    MIN_LAT = -90 
    MAX_LAT = 90

    class Meta:
        model = Station 
        fields = ['id', 'name', 'toll_per_cross', 'toll_per_extra_weight', 'location']
        read_only_fields = ['id'] 


    def validate_location(self, value:str):
        "location must be in this format: 'longitude,latitude' "
        point = value.split(',')
        if len(point) != 2:
            raise ValidationError("correct format of location= 'longitude,latitude' ")

        print(point)
        # convert to float 
        try:
            long = float(point[0].strip())
            lat  = float(point[1].strip())
        except Exception as e:
            print(e)
            raise ValidationError("correct format of location= 'longitude,latitude' ") 
            
        # check range of number
        if long > self.MAX_LONG or long < self.MIN_LONG:
            raise ValidationError(f"valid range of Longitude {self.MAX_LONG},{self.MIN_LONG}") 

        if lat > self.MAX_LAT or lat < self.MIN_LAT:
            raise ValidationError(f"valid range of latitude {self.MAX_LAT},{self.MIN_LAT}")

        return  create_point(long, lat)



class StationCrossSerializer(ModelSerializer):
    class Meta:
        model = StationCross 
        fields = ['id', 'station', 'vehicle', 'load', 'date','total_toll', 'paid']
        read_only_fields = ['id', 'total_toll', 'paid']

    def create(self, validated_data):
        print(validated_data)
        total_toll  = validated_data['station'].toll_per_cross

        if validated_data['load']:
            total_toll += validated_data['load'] * validated_data['station'].toll_per_extra_weight

        validated_data['total_toll'] = total_toll

        return super().create(validated_data)        
    
    def update(self, instance: StationCross, validated_data):
        total_toll  = validated_data['station'].toll_per_cross

        if validated_data['load']:
            total_toll += validated_data['load'] * validated_data['station'].toll_per_extra_weight

        instance.total_toll = total_toll 
        
        return super().update(instance, validated_data)
    

class TollPaymentSerializer(ModelSerializer):
    class Meta:
        model = TollPayment
        fields = ['id', 'station_cross', 'date']
        read_only_fields = ['id']

    def create(self, validated_data):
        # begin a transaction 
        with transaction.atomic():
            toll_payment = TollPayment() 
            toll_payment.station_cross = validated_data['station_cross']
            toll_payment.save() 

            station_cross: StationCross = toll_payment.station_cross
            vehicle = station_cross.vehicle
            vehicle_owner = VehicleOwner.objects.get(vehicle=vehicle)

            user: User = vehicle_owner.user
            user.total_toll_paid += toll_payment.station_cross.total_toll
            user.save()

            station_cross.paid = True 
            station_cross.save()

            return toll_payment
            # return super().create(validated_data)