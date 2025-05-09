from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status ,generics
from api.models import Avatar ,Space ,Element ,Map
from rest_framework.permissions import IsAuthenticated ,IsAdminUser, AllowAny
from rest_framework.exceptions import MethodNotAllowed
from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAdminUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import (
    AvatarsSerializer,
    SpaceSerializer,
    ElementSerializer,
    MapSerializer,
    UserSerializer
)

from django.http import HttpResponse

"""
Global Authentication Enforced Across All API Views

To ensure that all API views in this project require authentication, we've configured the global permission
class in the Django REST Framework settings:
The setting DEFAULT_PERMISSION_CLASSES in settings.py now includes IsAuthenticated.
"""


@api_view(['GET'])
def  AvatarView(request , pk=None):
    if request.method == 'GET':
        try:
            avatar=get_object_or_404(Avatar ,pk=pk)
            serializer =AvatarsSerializer(avatar)
            return Response (serializer.data ,status=status.HTTP_200_OK)
        except MethodNotAllowed:
            return Response ({"error":"Method not allowed"})


@api_view(['POST' ,'GET'])
def SpaceCreateAPIView(request):
    if request.method== 'POST':
        serializer=SpaceSerializer(data=request.data)
        if serializer.is_valid():
            try:
                space=serializer.save()
                return Response({"space_id": str(space.id)} ,status=status.HTTP_201_CREATED)

            except Exception as e :
                return Response ({"error": str(e)},status =status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class CreateSpaceAPIView(generics.CreateAPIView):
#     queryset = Space.objects.all()
#     serializer_class = SpaceSerializer
#     permission_classes = [IsAuthenticated] # only authenticated users can create spaces

#     def create(self, request, format=None):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             try:
#                 space = serializer.save()
#                 return Response(
#                     {
#                         "space_id": str(space.id),

#                      },
#                     status=status.HTTP_201_CREATED
#                 )
#             except Exception as e:
#                 return Response(
#                     {"error": str(e)},
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#         return Response(
#             {"error": serializer.errors},
#             status=status.HTTP_400_BAD_REQUEST
#         )


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

@api_view(['POST'])
# @permission_classes([IsAdminUser])
def AdminCreateAvatarView(request):
    """
    Creates a new Avatar.

    **Request Body Example:**
    ```json
    {
        "name": "Warrior",
        "image_url": "https://example.com/avatar.png"
    }
    ```
    Returns:
    - `201`: Avatar created successfully.
    - `400`: Bad request (validation error).
    - `500`: Internal server error.
    """
    if request.method== 'POST':
        serializer=AvatarsSerializer(data=request.data)
        if serializer.is_valid():
            try:
                avatar=serializer.save()
                return Response ({"message":"created successfully","avatar_id": avatar.id}, status=status.HTTP_201_CREATED)
            except Exception as e:  # Catch any unexpected errors
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"error": serializer.errors},status=status.HTTP_400_BAD_REQUEST)



# class CreateAPIView(generics.CreateAPIView):
#     """Create a new avatar"""
#     queryset=Avatar.objects.all()
#     serializer_class=AvatarsSerializer
#     permission_classes = [IsAdminUser]  # only admin can create avatars

#     def create(self, request, format=None):
#         serializer= self.get_serializer(data=request.data)

#         if serializer.is_valid():
#             try:
#                 avatar=serializer.save()
#                 return Response(
#                     {
#                         "avatar_id": avatar.id

#                      },
#                     status=status.HTTP_201_CREATED
#                 )

#             except Avatar.DoesNotExist:
#                 return Response({"detail": "Avatar not found"}, status=status.HTTP_404_NOT_FOUND)

        # return Response(
        #     {"error": serializer.errors},
        #     status=status.HTTP_400_BAD_REQUEST
        # )

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




def index(request):
    return HttpResponse("WebSocket server is running. Connect to /ws/ to use WebSockets.")

def room(request, room_name):
    return render(request, "api/room.html", {"room_name": room_name})

def metaverse(request):
    """Render the main metaverse interface"""
    return render(request, "api/metaverse.html")

def metaverse_rooms(request):
    """Render the metaverse rooms selection page"""
    return render(request, "api/rooms.html")

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    user = authenticate(email=email, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

