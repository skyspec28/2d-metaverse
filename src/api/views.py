from django.shortcuts import render
import requests
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from api.models import Avatar ,Space

from api.serializers import (
    AvatarsSerializer,
    SpaceSerializer,
    # SpaceElementSerializer,
    # ElementSerializer,
    # MapSerializeer,
    # MapELementSerializer,
    
)


class AvatarRetrieveView(APIView):
    def get (self , request, pk , format=None):
        try:
            avatar= Avatar.objects.get(pk=pk)
            serializer = AvatarsSerializer(avatar)
            return Response(serializer.data)
        except Avatar.DoesNotExist:
            return Response({"detail" : "Avatar not found "} ,status=status.HTTP_404_NOT_FOUND)
    

class SpaceView(APIView):
    def post (self , request, format=None):
        try:
            serializer= SpaceSerializer(data=request.data)
            if serializer.is_Valid():
                space=serializer.save()
                return Response({"space_id": str(space.id)},serializer.data , status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
            
        