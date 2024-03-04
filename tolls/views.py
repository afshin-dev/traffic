from rest_framework.decorators import api_view 
from rest_framework.request import Request
from rest_framework.response import Response
from utills import mongo
from django.conf import settings
from rest_framework import status
import json
from vehicles.models import VehicleType, Vehicle, VehicleOwner
from stations.models import StationCross 
from stations.serializers import StationCrossSerializer
# Create your views here.
TOLL_STATIONS_COLLECTION_NAME = "toll_stations"
ALL_NODES_COLLECTION_NAME = "all_nodes" 

MAX_DISTANCE_DIFAULT = 600 
VTYPE_DEFAULT = 1

@api_view(["GET"])
def vehicle_near_toll_station(request: Request, toll_station_id: int) -> Response:
    try:
        toll_station_id = int(toll_station_id)
    except:
        return Response("toll_station_id must be a int", status=status.HTTP_400_BAD_REQUEST)
    
    max_distance = request.query_params.get('distance')
    try:
        max_distance = int(max_distance)
    except:
        max_distance = MAX_DISTANCE_DIFAULT

    vtype_id = request.query_params.get('vtype_id')
    try:
        vtype_id = int(vtype_id)
    except:
        vtype_id = VTYPE_DEFAULT

    try:
        VehicleType.objects.get(pk=vtype_id)
    except VehicleType.DoesNotExist:
        Response({"error": "vehicle type  not found"},status=status.HTTP_404_NOT_FOUND)
        
    vehicles_by_vtype = Vehicle.objects.filter(vtype=vtype_id).only('id')
    vehicle_ids = [v.id for v in vehicles_by_vtype]

    client = mongo.get_client(settings.MONGO_HOST, settings.MONGO_PORT) 
    db = client[settings.MONGO_DATABASE]

    toll_stations = db[TOLL_STATIONS_COLLECTION_NAME]
    all_nodes = db[ALL_NODES_COLLECTION_NAME]

    # get all toll stations
    toll_station = toll_stations.find_one({'id' : toll_station_id})

    # print(toll_station)
    if toll_station:
        vehicle_near_toll_station_list = all_nodes.find({'car' : {'$in': vehicle_ids},
                                                         'location' : {"$nearSphere": {"$maxDistance": max_distance, "$geometry" : 
                                                                                       {"type" : "Point" , "coordinates" :toll_station['location']['coordinates'] }}}}, 
                                                         {'_id': 0})
        return Response(list(vehicle_near_toll_station_list))
    else:
        Response({"error": "toll station not found"},status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def user_tolls(request: Request, user_id :int)->Response:
    try:
        user_id = int(user_id)
    except:
        return Response({'errors' : 'invalid user id'}, status=status.HTTP_400_BAD_REQUEST)
        
    user_vehicles = VehicleOwner.objects.filter(user=user_id)
    user_vehicle_ids = [uv.id for uv in user_vehicles ]

    station_cross = StationCross.objects.filter(vehicle__in=user_vehicle_ids, paid=False)      
    station_cross_ser = StationCrossSerializer(station_cross, many=True)
    
    return Response(station_cross_ser.data)