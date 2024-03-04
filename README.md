# run application 
## install dependency
    - pip install -r requirements.txt
## migrate models to database 
    - py manage.py migrate  
## load fixtures (load data to database)
    - py manage.py loaddata user.json vehicle_type.json vehicles.json vehicle_owner.json       
## ensure mongodb run at localhost:27017
### if mongo is in another port and host change settings.MONGO_HOST and settings.MONGO_PORT 


## run development server 
    - py manage.py runserver     

## in navbar on http://127.0.0.1:8000/ click on `populate_db (only once)`
### or simply go to  http://127.0.0.1:8000/populate_db (this route populate mongodb traffic database) DONT RUN IT MORE THAN ONE TIME
    
## index creation on mongodb collection 
    - on fields all_nodes.location create a `2dsphere` index
    - on fields roads.geom create a `2dsphere` index 
        
## load fixture toll_stations (django signal must be trigger)   
### after running this fixture in mongodb `traffic` database must be a collection 
## named toll_stations with some initial documnets
    - py manage.py loaddata toll_stations.json


## run development server (if required) 
    - py manage.py runserver     

## READY TO test application 
### (some endpoint require admin permission) and request must be send 
### with admin token in this format
    Authorization: Token <>     