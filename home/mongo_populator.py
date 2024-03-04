from django.http.request import HttpRequest 
from django.http.response import HttpResponse , HttpResponseRedirect
# Create your views here.
from pymongo.database import Database 
from pymongo.collection import Collection
from pymongo.results import  InsertManyResult
import json
from pathlib import Path
from django.conf import settings
from utills import mongo 
from traffic.settings import BASE_DIR
import pymongo 





def populate_db(request: HttpRequest) -> HttpResponse:
    folder = BASE_DIR / "seed" 
    files = ( ( "roads.json" , "roads")  , ( "all_nodes.json", "all_nodes" ) )#, ("toll_stations.json" , "toll_stations") )
    
    for file in files:
        populate_data(folder / file[0], file[1])
    return HttpResponseRedirect('/')

def populate_data(p: str, col_name: str) -> InsertManyResult:
    """
      `p` path of file 
      `col_name` collection name 
    """
    file_path = Path(p) 
    client = mongo.get_client(settings.MONGO_HOST, settings.MONGO_PORT)
    traffic: Database = client.traffic
    
     
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
        collection: Collection = traffic[col_name] 
        result: InsertManyResult = collection.insert_many(data)

    # traffic['roads'].create_index(["geom", pymongo.GEOSPHERE])
    # traffic['all_nodes'].create_index(["location", pymongo.GEOSPHERE]) 

    return result

