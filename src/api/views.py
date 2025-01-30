from rest_framework.response import Response
from rest_framework import status ,generics
from api.models import Avatar ,Space ,Element ,SpaceElement
from rest_framework.permissions import IsAuthenticated ,IsAdminUser

from api.serializers import (
    AvatarsSerializer,
    SpaceSerializer,
    ElementSerializer
    # SpaceElementSerializer,
    # ElementSerializer,
    # MapSerializeer,
    # MapELementSerializer,
    
)

"""
Global Authentication Enforced Across All API Views

To ensure that all API views in this project require authentication, we've configured the global permission 
class in the Django REST Framework settings:
The setting DEFAULT_PERMISSION_CLASSES in settings.py now includes IsAuthenticated.
"""



class AvatarRetrieveView(generics.RetrieveAPIView):
    queryset = Avatar.objects.all()
    serializer_class = AvatarsSerializer
    

class CreateSpaceAPIView(generics.CreateAPIView):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    permission_classes = [IsAuthenticated] # only authenticated users can create spaces
    
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

  
# class RetrieveSpaceElementAPIView(generics.RetrieveAPIView):
#     queryset=SpaceElement.objects.all()
#     serializer_class=SpaceElementSerializer

#  ADMIN ONLY TASK
# ONLY ADMIN CAN ADD NEW MAP ,AVATARS ,STATTIC OBJECTS ,ELEMENTS ,
# CAN CHANGE DIMENSIONS WHEN ADDED 
# 

# only admins can add and delete element to a map 

class ElementCreateAPIView(generics.CreateAPIView):
    """Create a new element , element are static objects like chairs """

    queryset=Element.objects.all()
    serializer_class=ElementSerializer
    permission_classes = [IsAdminUser]

    def create(self, request, format=None):
        serializer= self.get_serializer(data=request.data)

        if serializer.is_valid():
            try:
                element=serializer.save()
                return Response(
                    {
                        "element_id":element.id
                     
                     },
                    status=status.HTTP_201_CREATED
                )

            except Element.DoesNotExist:
                return Response({"detail": "Element not found"}, status=status.HTTP_404_NOT_FOUND)
            
class ElementUpdateAPIView(generics.UpdateAPIView):
    """Update an existing element"""
    queryset=Element.objects.all()
    serializer_class=ElementSerializer

    def put (self, request, pk, format=None):
        try :
            element=Element.objects.get(id=pk)
            serializer=self.get_serializer(element, data=request.data)
        except Element.DoesNotExist:
            return Response({"detail": "Element not found"}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            element_obj=serializer.save()

