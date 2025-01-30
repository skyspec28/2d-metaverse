from django.shortcuts import render
import requests
import json
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status ,generics
from api.models import Avatar ,Space ,SpaceElement

from api.serializers import (
    AvatarsSerializer,
    SpaceSerializer,
    SpaceElementSerializer,
    # ElementSerializer,
    # MapSerializeer,
    # MapELementSerializer,
    
)

class AvatarRetrieveView(generics.RetrieveAPIView):
    queryset = Avatar.objects.all()
    serializer_class = AvatarsSerializer
    

class CreateSpaceAPIView(generics.CreateAPIView):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    
    def create(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            try:
                space = serializer.save()
                return Response(
                    {
                        "space_id": str(space.id),
                     
                     },
                    status=status.HTTP_201_CREATED
                )
            except Exception as e:
                return Response(
                    {"error": str(e)}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {"error": serializer.errors}, 
            status=status.HTTP_400_BAD_REQUEST
        )
        
    
class DestroySpaceView(generics.DestroyAPIView):
    def destroy (self , request, pk ,format=None):
        try:
            space =Space.objects.get(id=pk)
            space.delete()
            return Response({"detail": "Space deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
        except Space.DoesNotExist:
            return Response({"detail": "Space not found"}, status=status.HTTP_404_NOT_FOUND)
        

class SpaceListAPIView(generics.ListAPIView):
    queryset=Space.objects.all()
    serializer_class=SpaceSerializer

  
class RetrieveSpaceElementAPIView(generics.RetrieveAPIView):
    queryset=SpaceElement.objects.all()
    serializer_class=SpaceElementSerializer

# class MapView(APIView):
#     def get(self, request, map_id, format=None):
                