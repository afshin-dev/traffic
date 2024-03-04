from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver 
from .models import Station 
from utills import mongo
from django.conf import settings
from .utils import get_geojson_point
# {'signal': <django.db.models.signals.ModelSignal object at 0x0000026D962B3920>,
#   'instance': <Station: Station object (6)>,
#   'created': True, 'update_fields': None, 'raw': False, 'using': 'default'}


@receiver(post_save, sender=Station)
def upsert_station_to_mongo(sender, instance: Station, created,update_fields, **kwargs):
    """
        this receiver function only duplicate station data 
        to mongodb and it is only for demonstration of signal functionallity
    """
    COLLECTION = "toll_stations"
    client = mongo.get_client(settings.MONGO_HOST,settings.MONGO_PORT)
    db = client[settings.MONGO_DATABASE]
    coll = db[COLLECTION] 

    doc = {
            "id" : instance.pk , 
            "name" : instance.name, 
            "toll_per_cross": instance.toll_per_cross ,
            "toll_per_extra_weight": instance.toll_per_extra_weight,
            "location" : get_geojson_point(instance.location)
        }
    # new station 
    if created:
       
        try:
            result = coll.insert_one(doc)
            print(f"create station record to mongodb with id= {result.inserted_id}")
        except:
            print(f"error during inserting statoion = {instance.pk} to mongodb")
    else:
        # upsert 
        try:

            result = coll.replace_one({"id" : instance.pk} , doc, True)
            print(f"update station record to mongodb with id= {result.upserted_id}")

        except Exception as e: 
            print(f"error during upserting statoion = {instance.pk} to mongodb: {e}")




@receiver(post_delete, sender=Station)
def delete_station_from_mongodb(sender,instance: Station, **kwargs):
    """
        delete corresponding record in mongodb collection IF EXISTS
        its for demonstrations only 
    """
    COLLECTION = "toll_stations"
    client = mongo.get_client(settings.MONGO_HOST,settings.MONGO_PORT)
    db = client[settings.MONGO_DATABASE]
    coll = db[COLLECTION]

    try:
        result = coll.delete_one({"id": instance.pk})
        result.deleted_count and print(f"delete station from mongo for record station.pk = {instance.pk}")
    except Exception as e:
        print(f"durring delete data from mongo some error happend = {e}")    

