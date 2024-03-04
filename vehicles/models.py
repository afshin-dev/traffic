from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings 
# Create your models here.


class VehicleType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name
    

class Vehicle(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    COLORS = [
        ("RED", "Red" ),
        ("BLUE", "Blue"),
        ("GREEN", "Green"),
        ("BLACK", "Black"),
        ("YELLOW", "Yellow"), 
        ("White", "White") 
    ]
    vtype = models.ForeignKey(VehicleType, verbose_name ="Vehicle Type", on_delete=models.PROTECT)
    max_load = models.IntegerField(validators=[MinValueValidator(1)], blank=True,null=True)
    color = models.CharField(max_length=100, choices=COLORS) 
    last_long = models.FloatField(validators=[MinValueValidator(-180), MaxValueValidator(180)], null=True, blank=True)
    last_lat = models.FloatField(validators=[MinValueValidator(-90), MaxValueValidator(90)] ,null=True, blank=True)
    length = models.IntegerField(validators=[MinValueValidator(2)])

    def __str__(self) -> str:
        return  f"id={self.id}, {self.name}" if self.name else  f"id={self.id}, no-name"

class VehicleOwner(models.Model):
    # TODO: replace it with OneToOneField
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, unique=True) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)    

    class Meta:
        constraints = [models.UniqueConstraint(fields=('vehicle','user'), name="owner_vehicle_user_unique_together")]