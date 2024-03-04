from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin, User as f
from django.core.validators import  MinLengthValidator, MaxValueValidator, MinValueValidator 
from .managers import UserManager
# Create your models here.


MAX_NATIONAL_CODE_LENGTH = 10 
MIN_NATIONAL_CODE_LENGTH = 5


MIN_USER_AGE = 1
MAX_USER_AGE = 80

class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=200, blank=True, null=True)
    national_code = models.CharField(max_length=MAX_NATIONAL_CODE_LENGTH, validators=[MinLengthValidator(MIN_NATIONAL_CODE_LENGTH)], unique=True)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        # unique=True,
    )
    age = models.IntegerField(validators=[MinValueValidator(MIN_USER_AGE), MaxValueValidator(MAX_USER_AGE)]) 
    total_toll_paid = models.BigIntegerField(validators=[MinValueValidator(0)], default=0)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "national_code"
    REQUIRED_FIELDS = ["age"]

    def __str__(self):
        return f"nid={self.national_code} , email={self.email}"

    def has_perm(self, perm, obj=None):
        print(f"Debug:perm={perm}, obj={obj}")
        return True

    def has_module_perms(self, app_label):
        print(f"Debug:app_label={app_label}")
        return True

    @property
    def is_staff(self):
        return self.is_admin
