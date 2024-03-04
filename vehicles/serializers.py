from rest_framework.serializers import ModelSerializer, ValidationError
from .models import Vehicle, VehicleType, VehicleOwner

class VehicleSerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'name','vtype', 'max_load','color','last_long','last_lat','length']

class VehicleTypeSerializer(ModelSerializer):
    class Meta:
        model  = VehicleType 
        fields  = ['name', 'id'] 
        read_only_fields = ['id']   


class VehicleOwnerSerializer(ModelSerializer):
    HEAVY_VEHICLE_NAME = "heavy"

    class Meta:
        model = VehicleOwner
        fields = ['vehicle','user']  

    def validate(self, attrs):
        # for knowing witch user request to create a car/owner relationship
        user = self.context.get('user')
        if user == None :
            raise ValidationError('required user in serializer context')
        
        requested_vehicle_type = VehicleType.objects.get(id=attrs.get('vehicle').vtype.id)
        print(requested_vehicle_type)

        # getting all vehicles that a user owned
        userOwnedVehicles = VehicleOwner.objects.filter(user=attrs.get('user')) 

        # creating a id list of all vehicle ids
        vehiclesId = [uov.vehicle_id for uov in userOwnedVehicles]

        # actual vehicles
        actualVehicles = Vehicle.objects.select_related('vtype').filter(id__in=vehiclesId) 

        # check for heavy car in owned vehicles of user
        for av in actualVehicles:
            # check for if user already owned a heavy vehicle
            if av.vtype.name == self.HEAVY_VEHICLE_NAME and requested_vehicle_type.name == self.HEAVY_VEHICLE_NAME:
                raise ValidationError(f"user only allowd to owned one {self.HEAVY_VEHICLE_NAME} vehicle") 
            
            if av.id == attrs.get('vehicle').id:
                raise ValidationError(f"user already owned requested vehicle") 


        return attrs