from django.shortcuts import render
from rest_framework.viewsets import ViewSet 
from rest_framework.request import Request 
from rest_framework.response import Response 
from vehicles.models import Vehicle
from vehicles.serializers import VehicleSerializer
from django.urls import reverse 
from utills import mongo 
from django.conf import settings 
from pymongo.collection import Collection 
from pymongo.cursor import Cursor 
import json
# Create your views here.

HEAVY_VEHICLE_TYPE_NAME = 'heavy'
ALL_NODES_COLLECTION_NAME = "all_nodes"
ROADS_COLLECTION_NAME = "roads"

PAGE_SIZE  = 10
class HeavyVehicleOnViewSet(ViewSet):

    def list(self, request: Request) -> Response:
        heavy_vehicles = Vehicle.objects.filter(vtype__name=HEAVY_VEHICLE_TYPE_NAME)
        heavy_vehicles_ser = VehicleSerializer(heavy_vehicles, many=True)

        for hv in heavy_vehicles_ser.data:
            hv['under_20_road_cross'] = request._request.get_host() + reverse('roads-detail', args=(hv['id'],))
        return Response(heavy_vehicles_ser.data)
    
    def retrieve(self, request: Request, pk:int) -> Response:
        client = mongo.get_client(settings.MONGO_HOST, settings.MONGO_PORT)
        db = client[settings.MONGO_DATABASE]

        # page_number = request.query_params.get('page')

        # try:
        #     page_number = int(page_number)
        # except:
        #     page_number = 1 

        all_nodes: Collection = db[ALL_NODES_COLLECTION_NAME]
        roads: Collection = db[ROADS_COLLECTION_NAME]
        under_20_cross = list() 

        # find all record of car by pk
        nodes:Cursor = all_nodes.find({'car': int(pk)})#.skip(PAGE_SIZE * page_number).limit(PAGE_SIZE)

        for node in nodes:
            # for every record searchin in roads collection for finding a corresponding road
            #  and only pick the first road match in result
            near_roads = roads.find({'geom': {'$geoIntersects' : {'$geometry': {'type': 'Point' , 'coordinates': node['location']['coordinates']}}}}, {'_id': 0}).limit(1)

            # check if near_road width greater than 20
            for nr in near_roads:
                if nr['width'] < 20:
                    under_20_cross.append(nr)


        print(len(under_20_cross))

        return Response(under_20_cross)