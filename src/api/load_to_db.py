import uuid
# trib.auth.models import Userfrom django.con
from api.models import CustomUser, Space, SpaceElement, Element, Map, MapElement, Avatar, UserMetadata

custom_user = CustomUser.objects.create_user(
    username='john_doe',
    email='john@example.com',
    password='password123'
)


avatar = Avatar.objects.create(
    id=uuid.uuid4(),
    image_url='https://example.com/avatar.png',
    name='John Avatar'
)

user_metadata = UserMetadata.objects.create(
    user=custom_user,
    avatar=avatar
)

map_instance = Map.objects.create(
    width=1000,
    height=800,
    name='Sample Map',
    image_url='https://example.com/map.png',
    is_static=True
)


element = Element.objects.create(
    id=uuid.uuid4(),
    width=100,
    height=100,
    image_url='https://example.com/element.png'
)


space = Space.objects.create(
    id=uuid.uuid4(),
    name='Sample Space',
    width=500,
    height=500,
    map=map_instance,
    thumbnail='https://example.com/space_thumbnail.png'
)

space_element = SpaceElement.objects.create(
    element=element,
    space=space,
    x=10,
    y=20
)


map_element = MapElement.objects.create(
    map=map_instance,
    element=element,
    x=50,
    y=60
)


print(f"Created CustomUser: {custom_user}")
print(f"Created Avatar: {avatar}")
print(f"Created UserMetadata: {user_metadata}")
print(f"Created Map: {map_instance}")
print(f"Created Element: {element}")
print(f"Created Space: {space}")
print(f"Created SpaceElement: {space_element}")
print(f"Created MapElement: {map_element}")