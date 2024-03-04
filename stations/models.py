from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from vehicles.models import Vehicle 
# Create your models here.


class Station(models.Model):
    """
        a table for recording whole stations in cities
    """
    name = models.CharField(max_length=255, unique=True) 
    toll_per_cross = models.IntegerField(validators=[MinValueValidator(0)])
    toll_per_extra_weight = models.IntegerField(validators=[MinValueValidator(0)], default=300) 
    location = models.CharField(max_length=100)
    
    def __str__(self) -> str:
        return self.name




# only manage in sql with django orm 
class StationCross(models.Model):
    """
        this model is for recording station cross by car 
        without needs of geo location 
    """
    station = models.ForeignKey(Station, on_delete=models.CASCADE)

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)

    load = models.IntegerField(validators=[MinValueValidator(0)]) # how much extra weight vehicle of specific record reported
    date = models.DateTimeField(auto_now_add=True)

    total_toll = models.BigIntegerField() 
    paid = models.BooleanField(default=False)


class TollPayment(models.Model):
    """
        assume payment is public and accessible for everyone

        when create and delete: 
        update account of owner 
        update paid column in station cross
        
    """
    station_cross = models.ForeignKey(StationCross, models.PROTECT)
    date =  models.DateTimeField(auto_now_add=True)