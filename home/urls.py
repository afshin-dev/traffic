from django.urls import path 
from . import views 
from . import mongo_populator
urlpatterns = [
    path("", view=views.index, name="home.index"),
    path("populate_db/", view=mongo_populator.populate_db, name="home.populate_db")
]
