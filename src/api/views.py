from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status ,generics
from api.models import Avatar ,Space ,Element ,Map
from rest_framework.permissions import IsAuthenticated ,IsAdminUser
from rest_framework.exceptions import MethodNotAllowed

from api.serializers import (
    AvatarsSerializer,
    SpaceSerializer,
    ElementSerializer,
    MapSerializer

    
)

"""
Global Authentication Enforced Across All API Views

To ensure that all API views in this project require authentication, we've configured the global permission 
class in the Django REST Framework settings:
The setting DEFAULT_PERMISSION_CLASSES in settings.py now includes IsAuthenticated.
"""


@api_view(['GET' ,'POST'])
def  AvatarRetrieveView(request , pk=None):
    if request.method == 'GET':
        try:
            avatar=get_object_or_404(Avatar ,pk=pk)
            serializer =AvatarsSerializer(avatar)
            return Response (serializer.data)
        except MethodNotAllowed:
            return Response ({"error":"Method not allowed"})

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
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )
            
class ElementUpdateAPIView(generics.UpdateAPIView):
    """Update an existing element"""
    queryset=Element.objects.all()
    serializer_class=ElementSerializer
    permission_classes = [IsAdminUser]  # only admin can update elements

    def update (self, request, pk, format=None):
        try :
            element=Element.objects.get(id=pk)
            serializer=self.get_serializer(element, data=request.data)
        except Element.DoesNotExist:
            return Response({"detail": "Element not found"}, status=status.HTTP_404_NOT_FOUND)

        if serializer.is_valid():
            element_obj=serializer.save()
            image_url= element_obj.image_url
        
            return Response(
                {"image_url": image_url},
                status=status.HTTP_200_OK
            )

        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

class CreateAvatarAPIView(generics.CreateAPIView):
    """Create a new avatar"""
    queryset=Avatar.objects.all()
    serializer_class=AvatarsSerializer
    permission_classes = [IsAdminUser]  # only admin can create avatars

    def create(self, request, format=None):
        serializer= self.get_serializer(data=request.data)
         
        if serializer.is_valid():
            try:
                avatar=serializer.save()
                return Response(
                    {
                        "avatar_id": avatar.id
                     
                     },
                    status=status.HTTP_201_CREATED
                )

            except Avatar.DoesNotExist:
                return Response({"detail": "Avatar not found"}, status=status.HTTP_404_NOT_FOUND)
        
        return Response(
            {"error": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

class MapCreateAPIView(generics.CreateAPIView):
    """
    Creates a new map with elements. Admin only.
    Expects elements with both id and name.
    """
    queryset = Map.objects.all()
    serializer_class = MapSerializer
    permission_classes = [IsAdminUser]





    # def create(self, request, *args, **kwargs):
    #     elements_data = request.data.get('elements', [])
        
    #     # Validate elements data is a list
    #     if not isinstance(elements_data, list):
    #         return Response(
    #             {"error": "Elements must be a list"},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )

    #     # Quick validation of elements data
    #     for element in elements_data:
    #         if not isinstance(element, dict):
    #             return Response(
    #                 {"error": "Each element must be an object"},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )
            
    #         if 'id' not in element or 'name' not in element:
    #             return Response(
    #                 {"error": "Each element needs an id and name"},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )

    #     # Create the map
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     map_instance = serializer.save()

    #     # Add elements
    #     for element_data in elements_data:
    #         try:
    #             element = Element.objects.get(
    #                 id=element_data['id'],
    #                 name=element_data['name']
    #             )
    #             map_instance.elements.add(element)  # Changed from element to elements
    #         except Element.DoesNotExist:
    #             map_instance.delete()  # Clean up if something fails
    #             return Response(
    #                 {"error": f"Element {element_data['id']} not found"},
    #                 status=status.HTTP_400_BAD_REQUEST
    #             )

    #     return Response(serializer.data, status=status.HTTP_ 