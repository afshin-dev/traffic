from rest_framework.serializers import ModelSerializer , CharField
from .models import User, MAX_NATIONAL_CODE_LENGTH, MIN_NATIONAL_CODE_LENGTH
from rest_framework.exceptions import ValidationError

class UserCreationSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["national_code", "password", "age"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data) 
    
class UserReadSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["national_code", "age", "email"]


class UserLoginSerializer(ModelSerializer):
    national_code = CharField(max_length=MAX_NATIONAL_CODE_LENGTH, min_length=MIN_NATIONAL_CODE_LENGTH)
    class Meta:
        model = User 
        fields = ["national_code","password"]  
        
        extra_kwargs = {'password': {'write_only': True}}