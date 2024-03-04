from django.shortcuts import render
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet , ModelViewSet
from .serializers import UserCreationSerializer, UserReadSerializer, UserLoginSerializer 
from rest_framework import status
from .models import User
from django.contrib.auth import authenticate 
from rest_framework.authtoken.models import Token 

class UserViewSet(ViewSet):

    def get(self, request: Request) -> Response:
        """
            this method is only for convinience 
            creating a user at development and for demo
            that help api caller to creating user faster
        """
        return Response(  {
                "national_code" : "", 
                "age": 18 ,
                "password" : "" 
            }, status=status.HTTP_200_OK)
    

    def create(self, request: Request) -> Response:
        """
            sample json for creation a user 
            {
                "national_code" : "", 
                "age": 20 ,
                "password" : "" 
            }
        """
        ser = UserCreationSerializer(data=request.data)
        
        if ser.is_valid():
            new_user = ser.save()
            new_user_ser = UserReadSerializer(new_user)
            return Response(new_user_ser.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "user not valid"}, status=status.HTTP_400_BAD_REQUEST)
        
    

class UserLoginView(APIView):


    def get(self, request: Request) -> Response:
        """
            only for faster login
        """
        return Response({
            "national_code" : "",
            "password" : "" 
        }, status=status.HTTP_200_OK)
    

    def post(self, request: Request) -> Response:
        """
        assuming getting token successfully from server is login 
        
        sample login credential
        {
            "national_code" : "",
            "password" : "" 
        }
        """
        ser = UserLoginSerializer(data=request.data)

        if not ser.is_valid():
            return Response({"error": ser.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user  = User.objects.get(national_code=ser.validated_data.get('national_code'))
        except User.DoesNotExist:
            return Response({"error": "user does not exists"}, status=status.HTTP_400_BAD_REQUEST)
        

        user = authenticate(username=user.national_code, password=ser.validated_data.get('password'))
        if user == None:
            return Response({"error": "invalid credential"}, status=status.HTTP_401_UNAUTHORIZED) 
        

        token, created = Token.objects.get_or_create(user=user)


        return Response({"Authorization": f"Token {token.key}"})